import tensorflow as tf
Dataset.test()
dims, layers = 32, 2
# Creating the forward and backwards cells
lstm_fw_cell = tf.nn.rnn_cell.BasicLSTMCell(dims, forget_bias=1.0)
lstm_bw_cell = tf.nn.rnn_cell.BasicLSTMCell(dims, forget_bias=1.0)
# Pass lstm_fw_cell / lstm_bw_cell directly to tf.nn.bidrectional_rnn
# if only a single layer is needed
lstm_fw_multicell = tf.nn.rnn_cell.MultiRNNCell([lstm_fw_cell]*layers)
lstm_bw_multicell = tf.nn.rnn_cell.MultiRNNCell([lstm_bw_cell]*layers)

# tf.nn.bidirectional_rnn takes a list of tensors with shape 
# [batch_size x cell_fw.state_size], so separate the input into discrete
# timesteps.
_X = tf.unpack(state_below, axis=1)
# state_fw and state_bw are the final states of the forwards/backwards LSTM, respectively
outputs, state_fw, state_bw = tf.nn.bidirectional_rnn(lstm_fw_multicell,
                                                      lstm_bw_multicell,
                                                      _X,
                                                      dtype='float32')
