import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, LSTM, Bidirectional, Concatenate
from tensorflow.keras.datasets import imdb
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.callbacks import ModelCheckpoint
from fn1data import fn1data

# Load data
embedding_size = 50
num_title_embeddings = 13
num_body_embeddings = 500
data = fn1data()
train_title = data.train_titles
train_body = data.train_bodies
train_labels = data.train_labels
test_title = data.test_titles
test_body = data.test_bodies
test_labels = data.test_labels

# Create layers for model
input_title = keras.layers.Input(shape = (num_title_embeddings, embedding_size))

# BiLSTM layer that reads in a title input
flayer_title = LSTM(60, return_sequences=True, return_state=True)
blayer_title = LSTM(60, return_sequences=True, return_state=True, go_backwards=True)
lstm_title, fh_title, fc_title, bh_title, bc_title = Bidirectional(flayer_title, backward_layer=blayer_title)(input_title)

input_body = keras.layers.Input(shape = (num_body_embeddings, embedding_size))

# BiLSTM layer that reads in a body input and uses the previous layer's output as initial states
flayer_body = LSTM(60, return_sequences=True, return_state=True)
blayer_body = LSTM(60, return_sequences=True, return_state=True, go_backwards=True)
lstm_body, fh_body, fc_body, bh_body, bc_body = Bidirectional(flayer_body, backward_layer=blayer_body)\
    (input_body, initial_state=[fh_title, fc_title, bh_title, bc_title])

# Dense, Dropout and Dense (out) layers
dense1 = Dense(50, activation='relu')(keras.layers.average([fh_body, bh_body]))
dropout = Dropout(1e-3)(dense1)
output = Dense(4, activation='softmax')(dropout)

model = Model(inputs=[input_title, input_body], outputs=[output], name='BiLSTM_Model')

model.compile(loss=SparseCategoricalCrossentropy(),
              optimizer=Adam(learning_rate=1e-3),
              metrics=['accuracy'])

checkpoint = ModelCheckpoint("best_model.hdf5", monitor='loss', verbose=1,
    save_best_only=True, save_weights_only=False, mode='auto', period=1)

print("Training model on data")
history = model.fit([train_title, train_body],
                    train_labels,
                    batch_size=32,
                    epochs=20,
                    validation_split=0.3,
                    callbacks=[checkpoint])

print("Evaluating model on data")
test_scores = model.evaluate([test_title, test_body], y=test_labels, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])
