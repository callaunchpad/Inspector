import numpy as np
import tensorflow

import tensorflow.keras.layers as layers
from google.cloud import storage
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.losses import BinaryCrossentropy
import flask
from flask import jsonify, make_response, Flask, request
from os import path
import json
from nlp_tools import remove_punc, remove_stopwords, lemmatize, load_file

#### BILSTM Imports
from tensorflow import keras
from tensorflow.keras.layers import Dropout, LSTM, Bidirectional, Concatenate
from tensorflow.keras.datasets import imdb
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from search import search


app = Flask(__name__)

cnn = None
lstm = None

class CustomModel():
    def __init__(self):
        embedding_size = 50

        title_inputs = layers.Input(shape=(13, embedding_size), name='title')

        x = layers.Conv1D(8, 6, activation='relu', input_shape=(13, embedding_size))(title_inputs)
        x = layers.MaxPool1D(pool_size=4)(x)
        x = layers.Flatten()(x)
        title_outputs = layers.Dense(6, activation='relu')(x)

        ### TEXT BRANCH ###

        body_inputs = layers.Input(shape=(500, embedding_size), name='body')

        y = layers.Conv1D(42, 200, activation='relu', input_shape=(500, embedding_size))(body_inputs)
        y = layers.MaxPool1D(pool_size=4)(y)
        y = layers.Flatten()(y)
        body_outputs = layers.Dense(34, activation='relu')(y)

        ### CONCATENATE ###

        x = layers.concatenate([title_outputs, body_outputs])

        ### DENSE LAYERS ###

        x = layers.Dense(40)(x)
        x = layers.Dropout(.11)(x)
        x = layers.Dense(40)(x)
        x = layers.Dropout(.159)(x)
        output = layers.Dense(1, activation='sigmoid', name='output')(x)

        self.cnn = Model(inputs=[title_inputs, body_inputs], outputs=[output], name='CNN_model')
        self.cnn.compile(loss=BinaryCrossentropy(),
                      optimizer='Adam',
                      metrics=['accuracy'])


        ##### Create BILSTM
        embedding_size = 50
        num_title_embeddings = 15
        num_body_embeddings = 40

        # Create layers for model
        input_title = keras.layers.Input(shape = (num_title_embeddings, embedding_size))

        # BiLSTM layer that reads in a title input
        flayer_title = LSTM(60, return_state=True)
        blayer_title = LSTM(60, return_state=True, go_backwards=True)
        lstm_title, fh_title, fc_title, bh_title, bc_title = Bidirectional(flayer_title, backward_layer=blayer_title)(input_title)

        input_body = keras.layers.Input(shape = (num_body_embeddings, embedding_size))

        # BiLSTM layer that reads in a body input and uses the previous layer's output as initial states
        flayer_body = LSTM(60, return_state=True)
        blayer_body = LSTM(60, return_state=True, go_backwards=True)
        lstm_body, fh_body, fc_body, bh_body, bc_body = Bidirectional(flayer_body, backward_layer=blayer_body)\
            (input_body, initial_state=[fh_title, fc_title, bh_title, bc_title])

        # Dense, Dropout and Dense (out) layers
        dense1 = Dense(128, activation='relu')(keras.layers.average([fh_body, bh_body]))
        dropout1 = Dropout(1e-3)(dense1)
        dense2 = Dense(64, activation='relu')(dropout1)
        dropout2 = Dropout(1e-3)(dense2)
        output = Dense(4, activation='softmax')(dropout2)

        self.lstm = Model(inputs=[input_title, input_body], outputs=[output], name='BiLSTM_Model')

        self.lstm.compile(loss=SparseCategoricalCrossentropy(),
                      optimizer=Adam(learning_rate=1e-3),
                      metrics=['accuracy'])


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def process_input(title, body):
    arr_title = remove_punc(title)
    arr_title = remove_stopwords(arr_title)
    arr_title = lemmatize(arr_title)

    arr_body = remove_punc(body)
    arr_body = remove_stopwords(arr_body)
    arr_body = lemmatize(arr_body)

    empty_array = np.array([0]*50)

    print('pre_download_blob...')

    download_blob('cnn_model_inspector', 'emb_dict.pkl', '/tmp/emb_dict.pkl')

    print('post_download_blob...')

    emb_dict = load_file('/tmp/emb_dict.pkl')

    print('emb_dict loaded!')

    title_embedding = []
    for word in arr_title:
        if emb_dict.get(word) is None:
            title_embedding.append(emb_dict.get('unk')) # POTENTIALLY CHANGE WHAT TO APPEND
        else:
            title_embedding.append(emb_dict.get(word))
    if len(title_embedding) > 13:
        title_embedding = title_embedding[:13]
    elif len(title_embedding) < 13:
        while len(title_embedding) < 13:
            title_embedding.append(empty_array)

    body_embedding = []
    for word in arr_body:
        # if the word is OOV, append the unk vector
        if emb_dict.get(word) is None:
            body_embedding.append(emb_dict.get('unk')) # POTENTIALLY CHANGE WHAT TO APPEND
        else:
            body_embedding.append(emb_dict[word])

    if len(body_embedding) > 500:
        body_embedding = body_embedding[:500]
    elif len(body_embedding) < 500:
        while len(body_embedding) < 500:
            body_embedding.append(empty_array)

    return title_embedding, body_embedding

def nltk_test(inp):
    # looks like request.get_json() and the input.get_json() do the same thing
    print(request.get_json())
    print(inp.get_json())
    print(remove_punc("this, is some sample text."))
    arr = remove_punc("this, is some sample text.")
    arr = remove_stopwords(arr)
    arr = lemmatize(arr)
    print(arr)

def handler(request):
    print("beginning...")
    global cnn, lstm
    content = request.get_json()
    print('requested json: ', content)
    inputs = [0, 0]
    inputs[0], inputs[1] = process_input(content['title'], content['body'])

    lstm_articles = search(content['title']) #[(embedding, link)] of length 4
    
    print('inputs set up...')

    # cnn cache
    if cnn is None:
        download_blob('cnn_model_inspector', 'cnn.ckpt', '/tmp/weights.ckpt')
        cnn = CustomModel().cnn
        cnn.load_weights('/tmp/weights.ckpt')
        print('cnn model loaded...')

    cnn_predictions = cnn.predict([[inputs[0]], [inputs[1]]])
    # print('CNN Predictions: ', cnn_predictions)

    real_fake = {0: "Fake!", 1: "Real!"}
    final_cnn_pred = real_fake[np.round(cnn_predictions[0][0])]

    print("We predict the article is ", final_cnn_pred)

    # lstm cache
    if lstm is None:
        download_blob('cnn_model_inspector', 'lstm.ckpt', '/tmp/lstmweights.ckpt')
        lstm = CustomModel().lstm
        lstm.load_weights('/tmp/lstmweights.ckpt')
        print('bilstm model loaded...')

    print("The top 4 related articles have the following stances: ")
    for i in range(len(lstm_articles)):
        article = lstm_articles[i]
        lstm_prediction = lstm.predict([inputs[0]], [article[0]])
        print("Article", i, "'s stance is:", lstm_prediction)
        print("Article", i, "'s Link:", article[1])

    final_result = { 'result': final_cnn_pred }
    json_result = jsonify(probability=str(cnn_predictions[0][0]),
                          pred_class=str(np.round(cnn_predictions[0][0])))
    # print(json_result)
    # response = make_response(json_result)
    # print(response)
    # print(json.dumps(final_result), 200, {'Content-Type': 'application/json'})
    return json_result
