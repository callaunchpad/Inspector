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
from sklearn.utils import class_weight

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

# Add class weights to make training better
num_labels = [0, 0, 0, 0]
total = 0
for label in train_labels:
    num_labels[label] += 1
    total += 1
    
weight_for_unrelated = (1.0 / num_labels[0])*(total)
weight_for_discuss = (1.0 / num_labels[1])*(total)
weight_for_agree = (1.0 / num_labels[2])*(total)
weight_for_disagree = (1.0 / num_labels[3])*(total)
class_weights = {0: weight_for_unrelated, 1: weight_for_discuss, 2: weight_for_agree, 3: weight_for_disagree}
print(class_weights)

class_weights2 = class_weight.compute_class_weight('balanced',
                                                 np.unique(train_labels),
                                                 train_labels)
print(class_weights2)

print('title length:', len(train_title))

print('body length:', len(train_body))

# Create layers for model
input_title = keras.layers.Input(shape=(num_title_embeddings, embedding_size))

# BiLSTM layer that reads in a title input
flayer_title = LSTM(50, return_state=True)
blayer_title = LSTM(50, return_state=True, go_backwards=True)
lstm_title, fh_title, fc_title, bh_title, bc_title = Bidirectional(flayer_title, backward_layer=blayer_title)(input_title)

input_body = keras.layers.Input(shape=(num_body_embeddings, embedding_size))

# BiLSTM layer that reads in a body input and uses the previous layer's output as initial states
flayer_body = LSTM(50, return_state=True)
blayer_body = LSTM(50, return_state=True, go_backwards=True)
lstm_body, fh_body, fc_body, bh_body, bc_body = Bidirectional(flayer_body, backward_layer=blayer_body)\
    (input_body, initial_state=[fh_title, fc_title, bh_title, bc_title])

# Dense, Dropout and Dense (out) layers
# dense1 = Dense(128, activation='relu')(keras.layers.average([fh_body, bh_body]))
# dropout1 = Dropout(1e-3)(dense1)
# dense2 = Dense(64, activation='relu')(dropout1)
# dropout2 = Dropout(1e-3)(dense2)
# output = Dense(4, activation='softmax')(dropout2)
output = Dense(4, activation='softmax')(keras.layers.average([fh_body, bh_body]))

model = Model(inputs=[input_title, input_body], outputs=[output], name='BiLSTM_Model')

model.compile(loss=SparseCategoricalCrossentropy(),
              optimizer=Adam(learning_rate=5e-2),
              metrics=['accuracy'])

checkpoint = ModelCheckpoint("./LSTM_saves/lstm_smax.ckpt", monitor='val_acc', verbose=1,
    save_best_only=True, save_weights_only=False, mode='auto', period=1)

print("Training model on data")

history = model.fit([train_title, train_body],
                    train_labels,
                    batch_size=20,
                    epochs=20,
                    shuffle=True,
                    validation_split=0.3,
                    class_weight=class_weights,
                    callbacks=[checkpoint])

print("Evaluating model on data")
test_scores = model.evaluate([test_title, test_body], y=test_labels, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])
