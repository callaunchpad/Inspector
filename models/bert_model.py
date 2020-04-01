import bert
from tensorflow import keras
from os import path

model_dir = path.join(path.dirname(path.abspath(__file__)), 'uncased_L-12_H-768_A-12')
model_ckpt = path.join(model_dir, "bert_model.ckpt")
bert_params = bert.params_from_pretrained_ckpt(model_dir)
l_bert = bert.BertModelLayer.from_params(bert_params, name="bert")

max_seq_len = 128
l_input_ids = keras.layers.Input(shape=(max_seq_len,), dtype='int32')

# using the default token_type/segment id 0
output = l_bert(l_input_ids)                              # output: [batch_size, max_seq_len, hidden_size]
dense = keras.layers.Dense(2, activation='sigmoid')(output)
soft = keras.layers.Softmax(axis=-1)(dense)

model = keras.Model(inputs=l_input_ids, outputs=soft)
model.build(input_shape=(None, max_seq_len))

bert.load_bert_weights(l_bert, model_ckpt)      # should be called after model.build()

print('hi')