import bert
from bert import BertModelLayer
from tensorflow import keras


# l_bert = BertModelLayer(**BertModelLayer.Params(
#   vocab_size               = 16000,        # embedding params
#   use_token_type           = True,
#   use_position_embeddings  = True,
#   token_type_vocab_size    = 2,

#   num_layers               = 12,           # transformer encoder params
#   hidden_size              = 768,
#   hidden_dropout           = 0.1,
#   intermediate_size        = 4*768,
#   intermediate_activation  = "gelu",

#   adapter_size             = None,         # see arXiv:1902.00751 (adapter-BERT)

#   shared_layer             = False,        # True for ALBERT (arXiv:1909.11942)
#   embedding_size           = None,         # None for BERT, wordpiece embedding size for ALBERT

#   name                     = "bert"        # any other Keras layer params
# ))


model_dir = ".models/uncased_L-12_H-768_A-12"


bert_params = bert.params_from_pretrained_ckpt(model_dir)
l_bert = bert.BertModelLayer.from_params(bert_params, name="bert")

max_seq_len = 128
l_input_ids = keras.layers.Input(shape=(max_seq_len,), dtype='int32')
l_token_type_ids = keras.layers.Input(shape=(max_seq_len,), dtype='int32')

# using the default token_type/segment id 0
output = l_bert(l_input_ids)                              # output: [batch_size, max_seq_len, hidden_size]
dense = keras.layers.Dense(2, activation='sigmoid')(output)
soft = keras.layers.Softmax(axis=-1)(dense)

model = keras.Model(inputs=l_input_ids, outputs=soft)
model.build(input_shape=(None, max_seq_len))

# provide a custom token_type/segment id as a layer input
# output = l_bert([l_input_ids, l_token_type_ids])          # [batch_size, max_seq_len, hidden_size]
# model = keras.Model(inputs=[l_input_ids, l_token_type_ids], outputs=output)
# model.build(input_shape=[(None, max_seq_len), (None, max_seq_len)])

bert.load_bert_weights(l_bert, model_ckpt)      # should be called after model.build()
