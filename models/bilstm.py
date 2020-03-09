import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, LSTM, Bidirectional
from keras.datasets import imdb
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.callbacks import ModelCheckpoint
from fn1data import fn1data

# Create layers for model
input_title = keras.layers.Input(shape = (50, 1))

# BiLSTM layer that reads in a title input
forward_layer_title = LSTM(60, return_sequences=True, return_state=True)
backward_layer_title = LSTM(60, return_sequences=True, return_state=True, go_backwards=True)
lstm_title, forward_h_title, forward_c_title, backward_h_title, backward_c_title = Bidirectional(forward_layer_title, backward_layer=backward_layer_title)(input_title)

input_body = keras.layers.Input(shape = (50, 1))

# BiLSTM layer that reads in a body input and uses the previous layer's output as initial states
forward_layer_body = LSTM(60, initial_state=[forward_h_title, forward_c_title])
backward_layer_body = LSTM(60, return_sequences=True, return_states=True, go_backwards=True, initial_state=[backward_h_title, backward_c_title])
lstm_body, forward_h_body, forward_c_body, backward_h_body, backward_c_body = Bidirectional(forward_layer_body, backward_layer=backward_layer_body)(input_body)

# Dense, Dropout and Dense (out) layers
dense1 = Dense(50, activation='relu')(np.average(forward_h_body, backward_h_body))
dropout = Dropout(1e-3)(dense1)
output = Dense(4, activation='softmax')(dropout)

model = Model(inputs=[input_title, input_body], outputs=[output], name='BiLSTM Model')

model.compile(loss=SparseCategoricalCrossentropy(),
              optimizer=Adam(learning_rate=1e-3),
              metrics=['accuracy'])

checkpoint = ModelCheckpoint("best_model.hdf5", monitor='loss', verbose=1,
    save_best_only=True, save_weights_only=False, mode='auto', period=1)

# Loads the data
data = fn1data()
train_title = data.train_titles
train_body = data.train_bodies
train_labels = data.train_labels
test_title = data.test_titles
test_body = data.test_bodies
test_labels = data.test_labels

history = model.fit([train_title, train_body],
                    train_labels,
                    batch_size=32,
                    epochs=4,
                    validation_split=0.3,
                    callbacks=[checkpoint])

test_scores = model.evaluate([test_title, test_body], y=test_labels, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])
