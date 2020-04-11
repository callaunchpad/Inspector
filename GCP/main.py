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
app = Flask(__name__)

model = None

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

        self.model = Model(inputs=[title_inputs, body_inputs], outputs=[output], name='CNN_model')
        self.model.compile(loss=BinaryCrossentropy(),
                      optimizer='Adam',
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
    global model
    content = request.get_json()
    print('requested json: ', content)
    inputs = [0, 0]
    inputs[0], inputs[1] = process_input(content['title'], content['body'])
    print('inputs set up...')

    # Model load which only happens during cold starts
    if model is None:
        download_blob('cnn_model_inspector', 'cnn.ckpt', '/tmp/weights.ckpt')
        model = CustomModel().model
        model.load_weights('/tmp/weights.ckpt')
        print('model loaded...')

    predictions = model.predict([[inputs[0]], [inputs[1]]])
    print(predictions)
    print("Article is ", np.round(predictions[0][0]) )

    final_result = { 'result': str(np.round(predictions[0][0])) }
    json_result = jsonify(probability=str(predictions[0][0]),
                          pred_class=str(np.round(predictions[0][0])))
    # print(json_result)
    # response = make_response(json_result)
    # print(response)
    # print(json.dumps(final_result), 200, {'Content-Type': 'application/json'})
    return json_result
