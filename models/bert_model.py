import bert
from tensorflow import keras
from nlp_tools import save_file, load_file
from os import path
from tensorflow.keras.callbacks import ModelCheckpoint

bertdata_file = 'bertdata.pkl'
model_dir = path.join(path.dirname(path.abspath(__file__)), 'uncased_L-12_H-768_A-12')
model_ckpt = path.join(model_dir, "bert_model.ckpt")
bert_params = bert.params_from_pretrained_ckpt(model_dir)
l_bert = bert.BertModelLayer.from_params(bert_params, name="bert")

# Retrieve data from preloaded pkl file
bert_data = load_file(bertdata_file)
max_seq_len = bert_data.max_seq_len
train_data = bert_data.train_data
train_labels = bert_data.train_labels
test_data = bert_data.test_data
test_labels = bert_data.test_labels

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

# Train the model
checkpoint = ModelCheckpoint("./Bert_saves/bert.ckpt", monitor='val_loss', verbose=1,
    save_best_only=True, save_weights_only=False, mode='auto', period=1)

model.fit(
  train_data,
  train_labels,
  validation_split=0.1,
  batch_size=16,
  shuffle=True,
  epochs=5,
  callbacks=[checkpoint]
)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(test_data, test_labels, verbose=2)
print('Test loss:', test_loss)
print('Test accuracy:', test_accuracy)
