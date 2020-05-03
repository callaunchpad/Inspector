import numpy as np
import tensorflow as tf
from bilstm import create_bilstm
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
data = fn1data()
train_title = data.train_titles
train_body = data.train_bodies
train_labels = data.train_labels
test_title = data.test_titles
test_body = data.test_bodies
test_labels = data.test_labels

print('title length:', len(train_title))
print('body length:', len(train_body))

# Load pre-trained model
checkpoint_path = "./LSTM_saves/lstm_best.ckpt"
model = create_bilstm()
model.load_weights(checkpoint_path)

# Evaluate model (again)
print("Evaluating model on data")
test_scores = model.evaluate([test_title, test_body], y=test_labels, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])

# Test model
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
