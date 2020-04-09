import numpy as np
from tensorflow import keras
import time

from loader import load_data

from tensorflow.keras.optimizers import SGD
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras import layers
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Model

print("loading data...\n")
_, test_title, _, _, test_body, test_labels = load_data()
print("loaded data!")
embedding_size = 50
checkpoint_path = "./CNN_saves/cnn.ckpt"
def create_cnn():
    ### TITLE BRANCH ###
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
    model =  Model(inputs=[title_inputs, body_inputs], outputs=[output], name='CNN_model')
    model.compile(loss=BinaryCrossentropy(),
              optimizer='Adam',
              metrics=['accuracy'])
    return model

model = create_cnn()
model.load_weights(checkpoint_path)
print('model weights loaded')

results = model.evaluate([test_title, test_body], y=test_labels, verbose=2)
print('Test loss:', results[0])
print('Test accuracy:', results[1])

predictions = model.predict([test_title, test_body]).flatten()
# 1 means real, 0 means fake

# calculate true positive % i.e of the total number of fake articles, how many were predicted fake
num_tp = np.sum([1 for pred, lab in zip(predictions, test_labels) if round(pred) == lab and lab == 0])
tp = num_tp / (len(test_labels) - np.count_nonzero(test_labels))

# calculate true negative % i.e of the total number of real articles, how many were predicted real
num_tn = np.sum([1 for pred, lab in zip(predictions, test_labels) if round(pred) == lab and lab == 1])
tn = num_tn / np.count_nonzero(test_labels)

print("true positive (fake): {0}".format(tp))
print("true positive (real): {0}".format(tn))

# time for predicting 1 sample point
start = time.time()
predictions = model.predict([[test_title[0]], [test_body[0]]])
end = time.time()
print("time elapsed on CSUA GPU: {0}".format(end - start))
