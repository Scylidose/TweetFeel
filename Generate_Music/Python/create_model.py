from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Activation
from keras.callbacks import ModelCheckpoint

import os.path

def create_model(n_vocab, net_inp, model_type):

  model = Sequential()

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

  model.summary()
  
  return model

def model_fit(model, X_train, X_val, y_train, y_val, nb_epochs, batch_size, song_type, weights_dir):
    model_name = "best_model_"+ song_type.lower() + ".h5"

    weights_file_name = weights_dir + model_name

    if os.path.exists(weights_file_name):
        model.load_weights(weights_file_name)
    else:
        checkpoint = ModelCheckpoint(model_name, 
                                    monitor='loss',
                                    mode='min', 
                                    save_best_only=True,
                                    save_weights_only=True,
                                    verbose=0)

        callbacks_list = [checkpoint]
        model.fit(X_train, y_train,validation_data=(X_val,y_val), epochs=nb_epochs, batch_size=batch_size, callbacks=callbacks_list, verbose=1)

    return model