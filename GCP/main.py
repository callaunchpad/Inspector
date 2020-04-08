import numpy
import tensorflow

import tensorflow.keras.layers
from google.cloud import storage
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model
import flask
from flask import jsonify

model = None

class CustomModel(Model):
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

def handler(request):
    global model
    class_names = [0, 1]
    input = request

    # Model load which only happens during cold starts
    if model is None:
        download_blob('cnn_model_inspector', 'cnn.ckpt', '/tmp/weights.ckpt')
        model = CustomModel().model
        model.load_weights('/tmp/weights.ckpt')


    predictions = model.predict(input)
    print(predictions)
    print("Article is "+class_names[numpy.argmax(predictions)])

    return jsonify(class_names[numpy.argmax(predictions)])
