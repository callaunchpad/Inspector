import bert
from tensorflow import keras
from os import path

model_dir = path.join(path.dirname(path.abspath(__file__)), 'uncased_L-12_H-768_A-12')
model_ckpt = path.join(model_dir, "bert_model.ckpt")
bert_params = bert.params_from_pretrained_ckpt(model_dir)
l_bert = bert.BertModelLayer.from_params(bert_params, name="bert")

max_seq_len = 128

# Usually text inputs are tokenized and encoded based on a pre-set vocab. The steps are:
# 1. tokenize the text using the FullTokenizer from the bert module and vocab.txt
# 2. Add the tokens '[CLS]' and '[SEP]' at the begginning and end of the input text
# 3. convert the tokens into their numerical ids using FullTokenizer
# 4. Pad/truncate the sequences so that everything is max_seq_len
# you can print out each step to see if things look correct

l_input_ids = keras.layers.Input(shape=(max_seq_len,), dtype='int32')

# using the default token_type/segment id 0
output = l_bert(l_input_ids)                              # output: [batch_size, max_seq_len, hidden_size]

# The Bert output should be a vector of size [batch_size, hidden_size]. 
# Do this by getting only the first word encoding of the [CLS] token
# Take a look at Keras Lambda Layers for this.

dense = keras.layers.Dense(2, activation='sigmoid')(output)
soft = keras.layers.Softmax(axis=-1)(dense)

model = keras.Model(inputs=l_input_ids, outputs=soft)
model.build(input_shape=(None, max_seq_len))

bert.load_bert_weights(l_bert, model_ckpt)      # should be called after model.build()

print('hi')