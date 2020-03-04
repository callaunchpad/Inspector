import numpy as np
import matplotlib as plt
from tensorflow import keras

from loader import load_data

from keras.optimizers import SGD
from keras.losses import BinaryCrossentropy
from keras import layers
from keras.models import Model

train_title, test_title, train_labels, train_body, test_body, test_labels = load_data()


### TRAINING ###

### TITLE BRANCH ###

title_size = len(train_title)

title_inputs = layers.Input(shape=(title_size, ), name='title')

x = layers.Conv1D(8, title_size, activation='relu')(title_inputs)
x = layers.MaxPool1D(4)(x)
x = layers.Flatten()(x)
title_outputs = layers.Dense(6, activation='relu')(x)

### TEXT BRANCH ###

body_size = len(train_body)

body_inputs = layers.Input(shape=(body_size, ), name='body')

x = layers.Conv1D(42, body_size, activation='relu')(body_inputs)
x = layers.MaxPool1D(4)(x)
x = layers.Flatten()(x)
body_outputs = layers.Dense(34, activation='relu')(x)

### CONCATENATE ###

x = layers.concatenate([title_outputs, body_outputs])

### DENSE LAYERS ###

x = layers.Dense(40)(x)
x = layers.Dropout(.11)(x)
x = layers.Dense(40)(x)
x = layers.Dropout(.159)(x)
output = layers.Dense(2, name='output')(x)

model = Model(inputs=[title_inputs, body_inputs], outputs=[output], name='CNN_model')

model.compile(loss=BinaryCrossentropy(),
              optimizer=SGD(),
              metrics=['accuracy'])

history = model.fit({'title': train_title, 'body': train_body},
                    {'output': train_labels},
                    batch_size=32,
                    epochs=4,
                    validation_split=0.3)

test_scores = model.evaluate([test_title, test_body], test_labels, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])


