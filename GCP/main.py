import numpy
import tensorflow
import flask
import requests
import json
from flask import jsonify

from google.cloud import storage

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.datasets import imdb

import embeddings

bucket_name = 'inspector-test-model'
src_idx_name = 'cp.ckpt.index'
src_data_name = 'cp.ckpt.data-00000-of-00001'	
# We keep model as global variable so we don't have to reload it in case of warm invocations
model = None

word_to_idx = imdb.get_word_index()

def create_model():
    max_words = 20000
    hidden_size = 32
    sl_model = Sequential()
    sl_model.add(Embedding(max_words, hidden_size))
    sl_model.add(Bidirectional(LSTM(hidden_size, activation='tanh', dropout=0.2, recurrent_dropout=0.2)))
    sl_model.add(Dense(1, activation='sigmoid'))
    # sl_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return sl_model

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def handler(request):
    global model

    # Model load which only happens during cold starts
    if model is None:
        download_blob(bucket_name, src_idx_name, '/tmp/' + src_idx_name)
        download_blob(bucket_name, src_data_name, '/tmp/' + src_data_name)
        model = create_model()
        model.load_weights('/tmp/cp.ckpt')
    
    # get movie review text from request
    req_json = request.get_json()
    review = req_json.get('text')
    # process text into array to pass into the model
    tokens = embeddings.remove_punc(review)
    tokens = embeddings.remove_stopwords(tokens)
    model_input = embeddings.lemmatize(tokens)

    result = model.predict(model_input)
    # return str(req_json)
    response_data = { 'model_pred': result }
    return jsonify(response_data)


    # download_blob('<your_bucket_name>', 'tensorflow/test.png', '/tmp/test.png')
    # image = numpy.array(Image.open('/tmp/test.png'))
    # input_np = (numpy.array(Image.open('/tmp/test.png'))/255)[numpy.newaxis,:,:,numpy.newaxis]
    # predictions = model.call(input_np)
    # print(predictions)
    # print("Image is "+class_names[numpy.argmax(predictions)])
    
    # return class_names[numpy.argmax(predictions)]