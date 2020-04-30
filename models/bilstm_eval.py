import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, LSTM, Bidirectional, Concatenate
from tensorflow.keras.datasets import imdb
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.callbacks import ModelCheckpoint
from fn1data import fn1data
import time

# GPU stuff
# global boolean for using GPU or not
USE_GPU = True
if USE_GPU:
    tf.debugging.set_log_device_placement(True)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    print('GPUs available: ', gpus)

# Load data
embedding_size = 50
# num_title_embeddings = 13
# num_body_embeddings = 500
num_title_embeddings = 15
num_body_embeddings = 45

data = fn1data()
train_title = data.train_titles
train_body = data.train_bodies
train_labels = data.train_labels
test_title = data.test_titles
test_body = data.test_bodies
test_labels = data.test_labels

print('title length:', len(train_title))

print('body length:', len(train_body))

def create_bilstm():
    # Create layers for model
    input_title = keras.layers.Input(shape = (num_title_embeddings, embedding_size))

    # BiLSTM layer that reads in a title input
    flayer_title = LSTM(50, return_state=True)
    blayer_title = LSTM(50, return_state=True, go_backwards=True)
    lstm_title, fh_title, fc_title, bh_title, bc_title = Bidirectional(flayer_title, backward_layer=blayer_title)(input_title)

    input_body = keras.layers.Input(shape = (num_body_embeddings, embedding_size))

    # BiLSTM layer that reads in a body input and uses the previous layer's output as initial states
    flayer_body = LSTM(50, return_state=True)
    blayer_body = LSTM(50, return_state=True, go_backwards=True)
    lstm_body, fh_body, fc_body, bh_body, bc_body = Bidirectional(flayer_body, backward_layer=blayer_body)\
        (input_body, initial_state=[fh_title, fc_title, bh_title, bc_title])

    ### Dense, Dropout and Dense (out) layers
    # dense1 = Dense(128, activation='relu')(keras.layers.average([fh_body, bh_body]))
    # dropout1 = Dropout(1e-3)(dense1)
    # dense2 = Dense(64, activation='relu')(dropout1)
    # dropout2 = Dropout(1e-3)(dense2)
    # output = Dense(4, activation='softmax')(dropout2)

    # dropout = Dropout(0.1)(keras.layers.average([fh_body, bh_body]))
    output = Dense(4, activation='softmax')(keras.layers.average([fh_body, bh_body]))

    model = Model(inputs=[input_title, input_body], outputs=[output], name='BiLSTM_Model')

    model.compile(loss=SparseCategoricalCrossentropy(),
                optimizer=Adam(learning_rate=1e-3),
                metrics=['accuracy'])
    return model


checkpoint_path = "./LSTM_saves/lstm_best4.ckpt"
model = create_bilstm()
model.load_weights(checkpoint_path)
print("Evaluating model on data")
test_scores = model.evaluate([test_title, test_body], y=test_labels, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])

predictions = model.predict([test_title, test_body])
print(predictions)
print(test_labels)
print(len(predictions))
print(len(test_labels))

# compute confusion matrix. Rows are predicted, cols are actual
# labels = {'unrelated': 0, 'discus': 1, 'agree': 2, 'disagree': 3}
conf_matrix = [[0] * 4 for _ in range(4)]
for i in range(4):
    for j in range(4):
        # number predictions made for class i when true class was j
        # (of the number of points in j, how many were classified as i?)
        num = np.sum([1 for pred, lab in zip(predictions, test_labels) \
                if np.argmax(pred) == i and lab == j])
        # matrix entry is num / (total number of labels in class j)
        conf_matrix[i][j] = num / np.sum(test_labels == j)

print(conf_matrix)

# time for predicting 1 sample point
start = time.time()
predictions = model.predict([[test_title[0]], [test_body[0]]])
end = time.time()
print("time elapsed on CSUA GPU: {0}".format(end - start))

