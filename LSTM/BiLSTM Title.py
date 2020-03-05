import numpy as np
from tensorflow import keras
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from keras.datasets import imdb


title_input = keras.layers.Input(shape = (50, 1))

forward_layer = LSTM(60)
backward_layer = LSTM(60, activation='tanh', return_sequences=False, go_backwards=True)
x = Bidirectional(forward_layer, backward_layer=backward_layer)
