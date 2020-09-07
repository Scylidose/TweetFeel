from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Activation, GRU, Bidirectional
from keras.callbacks import ModelCheckpoint

import os.path

def create_model(n_vocab, net_inp, model_type):

  model = Sequential()
  if model_type == "LSTM":
    model.add(LSTM(
            512,
            input_shape=(net_inp.shape[1], net_inp.shape[2]),
            return_sequences=True
        ))
    model.add(Dropout(0.2))
    model.add(LSTM(256, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

  elif model_type == "GRU":
    model.add(Bidirectional(GRU(256, input_shape=(net_inp.shape[1], net_inp.shape[2]))))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
  
  elif model_type == "FINAL":
    model.add(Bidirectional(GRU(256, input_shape=(net_inp.shape[1], net_inp.shape[2]), return_sequences=True)))
    model.add(Dropout(0.2))
    model.add(Bidirectional(GRU(256, input_shape=(net_inp.shape[1], net_inp.shape[2]))))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
  
  return model

def model_fit(model, X_train, y_train, nb_epochs, batch_size, song_type, nb, model_type, weights_dir):
    model_name = "best_model_"+ song_type.lower()

    weights_file_name = weights_dir + model_name

    if os.path.exists(weights_file_name):
      if model_type == "FINAL":
        model.load_weights(weights_file_name + "_n"+ nb +".h5")
      else:
        model.load_weights(weights_file_name + ".h5")
    else:
        model.fit(X_train, y_train, epochs=nb_epochs, batch_size=batch_size, verbose=1)

    return model