import numpy as np
import matplotlib as plt
from tensorflow import keras

from keras import layers
from keras.models import Model


### TITLE BRANCH ###

title_size = 500 # TO BE FOUND

title_inputs = layers.Input(shape=(title_size, )) # TO BE GIVEN

x = layers.Conv1D(8, title_size, activation='relu')(title_inputs)
x = layers.MaxPool1D(4)(x)
x = layers.Flatten()(x)
title_outputs = layers.Dense(6, activation='relu')(x)

### TEXT BRANCH ###

text_size = 500 # TO BE FOUND

text_inputs = layers.Input(shape=(text_size, )) # TO BE GIVEN

x = layers.Conv1D(42, text_size, activation='relu')(text_inputs)
x = layers.MaxPool1D(4)(x)
x = layers.Flatten()(x)
text_outputs = layers.Dense(34, activation='relu')(x)

### CONCATENATE ###

x = layers.concatenate([title_outputs, text_outputs])

### DENSE LAYERS ###

x = layers.Dense(40)(x)
x = layers.Dropout(.11)(x)
x = layers.Dense(40)(x)
x = layers.Dropout(.159)(x)
output = layers.Dense(2)(x)

