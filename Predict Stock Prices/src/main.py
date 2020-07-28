#!/usr/bin/python3

import yfinance as yf

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

import os.path
from os import path

from keras.layers.core import Dense, Activation, Dropout
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from tensorflow import keras


def transf_list(lst):
    return [[el] for el in lst]


def fetch_data(data_path, currency):
    curr = yf.Ticker(currency)

    max_range_curr = curr.history(period="max")
    max_range_curr.to_csv(data_path, index = False)

def load_data(data_path):
    data = pd.read_csv(data_path).dropna().reset_index(drop=True)
    data = data.drop(['Date','Dividends', 'Stock Splits'], axis=1, errors='ignore')

    print(data.shape)

    return data

def preprocess_data(data, min_max_scaler):
    X = transf_list(data.iloc[:, 0])
    y = data.iloc[:, [3]].values.tolist()

    x_scaled = min_max_scaler.fit_transform(X)
    y_scaled = min_max_scaler.fit_transform(y)

    
    sliced_day = len(X) - 365

    X_train = x_scaled[0:sliced_day]
    X_test = x_scaled[sliced_day:-1]

    y_train = y_scaled[0:sliced_day]
    y_test = y_scaled[sliced_day:-1]

    X_train = X_train.reshape(X_train.shape[0],  X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    print(X_train.shape)

    return [(X_train, y_train), (X_test, y_test)]

def predict_stock():
    data_path = "../data/BAT-CAD.csv"
    currency = "BAT-CAD"

    fetch_data(data_path, currency)

    data = load_data(data_path)

    min_max_scaler = preprocessing.MinMaxScaler()

    [(X_train, y_train), (X_test, y_test)] = preprocess_data(data, min_max_scaler)

    if(path.exists("model/model") == False):

        model = Sequential()

        model.add(LSTM(units = 100, return_sequences = True, input_shape = (X_train.shape[1], 1)))
        model.add(Dropout(0.3))
        model.add(LSTM(units = 50, return_sequences = True))
        model.add(Dropout(0.3))
        model.add(LSTM(units = 50))
        model.add(Dropout(0.3))
        model.add(Dense(units = 1, activation='linear'))

        model.compile(optimizer = 'adam', loss = 'mean_squared_error')

        print("------- SAVING MODEL --------")

        model.save('model/model')
    
    else:
        print("------- LOADING MODEL --------")
        model = keras.models.load_model("model/model")

    model.fit(X_train, y_train, epochs = 10, batch_size = 32)

    y_pred = model.predict(X_test)



    unscaled_y_pred = min_max_scaler.inverse_transform(y_pred)
    unscaled_y_test = min_max_scaler.inverse_transform(y_test)

    return (unscaled_y_pred, unscaled_y_test)


if __name__ == "__main__":
    predict_stock()