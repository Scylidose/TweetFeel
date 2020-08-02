#!/usr/bin/python3

import numpy as np
import pandas as pd
from sklearn import preprocessing

import os.path
from os import path

from keras.layers.core import Dense, Activation, Dropout
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from sklearn.metrics import r2_score

from tensorflow import keras
from keras import backend as K


def transf_list(lst):
    return [[el] for el in lst]

def load_data(data_path, cryptocurrency):
    data = pd.read_csv(data_path + cryptocurrency + '.csv').dropna().reset_index(drop=True)

    return data

def preprocess_data(data, min_max_scaler):
    X = transf_list(data.iloc[:, 1])
    y = data.iloc[:, [4, 5]].values.tolist()

    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(X)
    y_scaled = min_max_scaler.fit_transform(y)


    train_sliced_day = round(len(X) * 0.6)
    valid_sliced_day = round(train_sliced_day + len(X) * 0.2)

    X_train = x_scaled[0:train_sliced_day]
    X_valid = x_scaled[train_sliced_day:valid_sliced_day]
    X_test = x_scaled[valid_sliced_day:]

    y_train = y_scaled[0:train_sliced_day]
    y_valid = y_scaled[train_sliced_day:valid_sliced_day]
    y_test = y_scaled[valid_sliced_day:]

    X_train = X_train.reshape(X_train.shape[0],  X_train.shape[1], 1)
    X_valid = X_valid.reshape(X_valid.shape[0],  X_valid.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    return [(X_train, y_train), (X_valid, y_valid),(X_test, y_test), min_max_scaler]

def predict_stock(data_path, cryptocurrency):

    data = load_data(data_path, cryptocurrency)

    min_max_scaler = preprocessing.MinMaxScaler()

    [(X_train, y_train), (X_valid, y_valid),(X_test, y_test), min_max_scaler] = preprocess_data(data, min_max_scaler)

    K.clear_session()

    accuracy, y_pred = get_model(X_train, y_train, X_test, y_test)

    K.clear_session()

    unscaled_y_pred = min_max_scaler.inverse_transform(y_pred)
    unscaled_y_test = min_max_scaler.inverse_transform(y_test)

    today = unscaled_y_pred[len(unscaled_y_pred) - 1]

    return [(unscaled_y_pred[:-1], unscaled_y_test, today), accuracy]

def get_model(X_train, y_train, X_test, y_test,
          unit= 150, dropout_prob=0.3, opt='adam', epochs=20, batch_size=128):
    
    model = Sequential()

    model.add(LSTM(units = unit, return_sequences = True, input_shape = (X_train.shape[1], 1)))
    model.add(Dropout(dropout_prob))
    model.add(LSTM(units = unit, return_sequences = True))
    model.add(Dropout(dropout_prob))
    model.add(LSTM(units = unit, return_sequences = True))
    model.add(Dropout(dropout_prob))
    model.add(LSTM(units = unit))
    model.add(Dropout(dropout_prob))
    model.add(Dense(units = 2))

    model.compile(optimizer = opt, loss = 'mean_squared_error')

    model.fit(X_train, y_train, epochs = epochs, batch_size = batch_size, verbose=0)
    y_pred = model.predict(X_test)

    accuracy = round(r2_score(y_test,y_pred)*100, 3)
    
    return accuracy, y_pred
