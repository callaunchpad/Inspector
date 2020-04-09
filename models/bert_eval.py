import bert
from tensorflow import keras
from nlp_tools import save_file, load_file
from os import path
import numpy as np
import time
checkpoint_path = "./Bert_saves/bert.ckpt"

# Retrieve data from preloaded pkl file

bertdata_file = 'bertdata.pkl'

bert_data = load_file(bertdata_file)
max_seq_len = bert_data.max_seq_len
train_data = bert_data.train_data
train_labels = bert_data.train_labels
test_data = bert_data.test_data
test_labels = bert_data.test_labels

def create_bert():
    model_dir = path.join(path.dirname(path.abspath(__file__)), 'uncased_L-12_H-768_A-12')
    model_ckpt = path.join(model_dir, "bert_model.ckpt")
    bert_params = bert.params_from_pretrained_ckpt(model_dir)
    l_bert = bert.BertModelLayer.from_params(bert_params, name="bert")

    # Create the model
    l_input_ids = keras.layers.Input(shape=(max_seq_len,), dtype='int32', name='input_ids')
    bert_output = l_bert(l_input_ids)
    cls_output = keras.layers.Lambda(lambda seq: seq[:, 0, :])(bert_output)
    dense = keras.layers.Dense(2, activation='sigmoid')(cls_output)
    soft = keras.layers.Softmax(axis=-1)(dense)

    model = keras.Model(inputs=l_input_ids, outputs=soft, name='Bert_model')
    model.build(input_shape=(None, max_seq_len))

    bert.load_bert_weights(l_bert, model_ckpt)

    model.summary()

    # Compile the model
    model.compile(
        optimizer=keras.optimizers.Adam(1e-5),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[keras.metrics.SparseCategoricalAccuracy(name="acc")]
    )
    return model

model = create_bert()
model.load_weights(checkpoint_path)
print('model weights loaded')

test_loss, test_accuracy = model.evaluate(test_data, test_labels, verbose=2)
print('Test loss:', test_loss)
print('Test accuracy:', test_accuracy)

predictions = model.predict(test_data)
print(test_data)
print(test_data[0])
print(predictions)
print(test_labels)
print(len(predictions))
print(len(test_labels))

# 1 means real, 0 means fake
# calculate true positive % i.e of the total number of fake articles, how many were predicted fake
num_tp = np.sum([1 for pred, lab in zip(predictions, test_labels) if np.argmax(pred) == lab and lab == 0])
tp = num_tp / (len(test_labels) - np.count_nonzero(test_labels))

# calculate true negative % i.e of the total number of real articles, how many were predicted real
num_tn = np.sum([1 for pred, lab in zip(predictions, test_labels) if np.argmax(pred) == lab and lab == 1])
tn = num_tn / np.count_nonzero(test_labels)

print("true positive (fake): {0}".format(tp))
print("true positive (real): {0}".format(tn))

# time for predicting 1 sample point
start = time.time()
print(test_data[0].shape)
predictions = model.predict(np.array([test_data[0]]))
end = time.time()
print("time elapsed on CSUA GPU: {0}".format(end - start))

