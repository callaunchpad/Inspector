import tensorflow as tf
from bilstm import create_bilstm
from tensorflow.keras.callbacks import ModelCheckpoint
from fn1data import fn1data

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

# Create class weights to make training more even
num_labels = [0, 0, 0, 0]
total = 0
for label in train_labels:
    num_labels[label] += 1
    total += 1

weight_for_unrelated = 1 / num_labels[0] * total
weight_for_discuss = 1 / num_labels[1] * total
weight_for_agree = 1 / num_labels[2] * total
weight_for_disagree = 1 / num_labels[3] * total

# Line below gives {0: 1.368895869096753, 1: 5.617356115107913, 2: 13.525442078671958, 3: 57.04566210045662}
# class_weights = {0: weight_for_unrelated, 1: weight_for_discuss, 2: weight_for_agree, 3: weight_for_disagree}

# Adjusted class weights that gives optimal all-round results
class_weights = {0: 1, 1: 5, 2: 14.5, 3: 60}
print(class_weights)

model = create_bilstm()
checkpoint = ModelCheckpoint("./LSTM_saves/lstm_best.ckpt", monitor='val_acc', verbose=1,
                             save_best_only=True, save_weights_only=False, mode='auto', period=1)

# Train model
print("Training model on data")
history = model.fit([train_title, train_body],
                    train_labels,
                    batch_size=20,
                    epochs=20,
                    shuffle=True,
                    validation_split=0.3,
                    class_weight=class_weights,
                    callbacks=[checkpoint])

# Evaluate model
print("Evaluating model on data")
test_scores = model.evaluate([test_title, test_body], y=test_labels, verbose=2)
print('Test loss:', test_scores[0])
print('Test accuracy:', test_scores[1])
