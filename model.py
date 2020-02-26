import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import Sequential
import os
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.layers import Bidirectional
import numpy as np

# LSTM format for sentiment analysis on movie reviews

# for saving the model
checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

max_words = 20000
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_words)

# print("X_train length: ", len(x_train))
# print("X_test length: ", len(x_test))

word_to_index = imdb.get_word_index()
index_to_word = {v: k for k, v in word_to_index.items()}

# print(x_train[0])
# print(" ".join([index_to_word[x] for x in x_train[0]]))

# print("Min value:", min(y_train), "Max value:", max(y_train))

average_length = np.mean([len(x) for x in x_train])
median_length = sorted([len(x) for x in x_train])[len(x_train) // 2]

# print("Average sequence length: ", average_length)
# print("Median sequence length: ", median_length)

max_sequence_length = 180

x_train = sequence.pad_sequences(x_train, maxlen=max_sequence_length, padding='post', truncating='post')
x_test = sequence.pad_sequences(x_test, maxlen=max_sequence_length, padding='post', truncating='post')

# print('X_train shape: ', x_train.shape)

# Single layer LSTM example

hidden_size = 32

sl_model = Sequential()
sl_model.add(Embedding(max_words, hidden_size))
sl_model.add(Bidirectional(LSTM(hidden_size, activation='tanh', dropout=0.2, recurrent_dropout=0.2)))
sl_model.add(Dense(1, activation='sigmoid'))
sl_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

epochs = 3

sl_model.fit(x_train[:1000], y_train[:1000], epochs=epochs, shuffle=True, callbacks=[cp_callback])
loss, acc = sl_model.evaluate(x_test, y_test)

# d_model = Sequential()
# d_model.add(Embedding(max_words, hidden_size))
# d_model.add(Bidirectional(LSTM(hidden_size, activation='tanh', dropout=0.2, recurrent_dropout=0.2, return_sequences=True)))
# d_model.add(Bidirectional(LSTM(hidden_size, activation='tanh', dropout=0.2, recurrent_dropout=0.2)))
# d_model.add(Dense(1, activation='sigmoid'))

# d_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# d_model.summary()

# d_model.fit(x_train, y_train, epochs=epochs, shuffle=True, callbacks=[cp_callback])
# d_loss, d_acc = d_model.evaluate(x_test, y_test)

print('Single layer model -- ACC {} -- LOSS {}'.format(acc, loss))
# print('Double layer model -- ACC {} -- LOSS {}'.format(d_acc, d_loss))

