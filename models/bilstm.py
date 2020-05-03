from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, LSTM, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy

embedding_size = 50
num_title_embeddings = 15
num_body_embeddings = 45


def create_bilstm():
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

    output = Dense(4, activation='softmax')(keras.layers.average([fh_body, bh_body]))
    model = Model(inputs=[input_title, input_body], outputs=[output], name='BiLSTM_Model')
    model.compile(loss=SparseCategoricalCrossentropy(),
                  optimizer=Adam(learning_rate=1e-3),
                  metrics=['accuracy'])

    return model
