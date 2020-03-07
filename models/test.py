import numpy as np
import matplotlib as plt
from tensorflow import keras

from loader import load_data

from tensorflow.keras.optimizers import SGD
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras import layers
from tensorflow.keras.models import Model

print("loading data...\n")
train_title, test_title, train_labels, train_body, test_body, test_labels = load_data()
print("loaded data!")

### TRAINING ###

### TITLE BRANCH ###

print(np.shape(test_labels))

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
output = layers.Dense(1, name='output')(x)

model = Model(inputs=[title_inputs, body_inputs], outputs=[output], name='CNN_model')

model.compile(loss=BinaryCrossentropy(),
              optimizer=SGD(momentum=0.303, learning_rate=0.240),
              metrics=['accuracy'])

print("begin training... \n")
history = model.fit([train_title, train_body],
                    train_labels,
                    batch_size=32,
                    epochs=4,
                    validation_split=0.3)

test_scores = model.evaluate([test_title, test_body], y=test_labels, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])


