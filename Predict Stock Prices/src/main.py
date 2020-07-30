#!/usr/bin/python3

import yfinance as yf

import numpy as np
import pandas as pd
from sklearn import preprocessing

import os.path
from os import path

import glob
import random

from keras.layers.core import Dense, Activation, Dropout
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM

from tensorflow import keras
from keras import backend as K


def transf_list(lst):
    return [[el] for el in lst]


def fetch_currency(data_path, cryptocurrency):
    files = glob.glob(data_path+"*.csv")
    crypto_file = data_path+'cryptocurrencies.csv'

    for i in range(len(files)):
        if(files[i] != crypto_file):
            os.remove(files[i])

    curr = yf.Ticker(cryptocurrency)

    max_range_curr = curr.history(period="max")
    max_range_curr.to_csv(data_path + cryptocurrency + '.csv', index = False)

def load_data(data_path, cryptocurrency):
    data = pd.read_csv(data_path + cryptocurrency + '.csv').dropna().reset_index(drop=True)
    data = data.drop(['Date','Dividends', 'Stock Splits'], axis=1, errors='ignore')

    return data

def preprocess_data(data, min_max_scaler):
    X = transf_list(data.iloc[:, 0])
    y = data.iloc[:, [3]].values.tolist()

    x_scaled = min_max_scaler.fit_transform(X)
    y_scaled = min_max_scaler.fit_transform(y)

    
    sliced_day = len(X) - 365

    X_train = x_scaled[0:sliced_day]
    X_test = x_scaled[sliced_day:]

    y_train = y_scaled[0:sliced_day]
    y_test = y_scaled[sliced_day:-1]

    X_train = X_train.reshape(X_train.shape[0],  X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    return [(X_train, y_train), (X_test, y_test)]

def predict_stock(data_path, cryptocurrency):

    fetch_currency(data_path, cryptocurrency)

    data = load_data(data_path, cryptocurrency)

    min_max_scaler = preprocessing.MinMaxScaler()

    [(X_train, y_train), (X_test, y_test)] = preprocess_data(data, min_max_scaler)

    K.clear_session()

    model = get_model(X_train, cryptocurrency)

    model.compile(optimizer = 'adam', loss = 'mean_squared_error')

    model.fit(X_train, y_train, epochs = 10, batch_size = 32)
    
    y_pred = model.predict(X_test)

    y_pred_future = predict_future(model, X_test[-1], y_pred[-1])
    unscaled_X_pred_future = min_max_scaler.inverse_transform(y_pred_future.iloc[:,0].to_list())
    unscaled_y_pred_future = min_max_scaler.inverse_transform(y_pred_future.iloc[:,1].to_list())

    K.clear_session()

    unscaled_y_pred = min_max_scaler.inverse_transform(y_pred)
    unscaled_y_test = min_max_scaler.inverse_transform(y_test)

    today = unscaled_y_pred[len(unscaled_y_pred) - 1]

    return [(unscaled_y_pred[:-1], unscaled_y_test, today), (unscaled_X_pred_future, unscaled_y_pred_future)]

def get_model(X_train, cryptocurrency):
    model = Sequential()

    model.add(LSTM(units = 100, return_sequences = True, input_shape = (X_train.shape[1], 1)))
    model.add(Dropout(0.3))
    model.add(LSTM(units = 50, return_sequences = True))
    model.add(Dropout(0.3))
    model.add(LSTM(units = 50))
    model.add(Dropout(0.3))
    model.add(Dense(units = 1, activation='linear'))

    return model

def predict_future(model, X_today, y_today):
    nb_days = 30
    y_pred_future = pd.DataFrame(data={'Predicted Open': [X_today], 'Predicted Close': [y_today]})

    for i in range(nb_days):
        Adj_close = y_pred_future.iloc[-1:, 1].values
        
        random_adj = random.randint(1, 5)

        if(random.randint(0, 1) == 0):
            Adj_close += Adj_close * (random_adj/100)
        else:
            Adj_close -= Adj_close * (random_adj/100)


        X_tomorrow = np.asarray([[Adj_close]])
        y_pred = model.predict(X_tomorrow)

        y_pred_future.loc[len(y_pred_future)] = [Adj_close, y_pred[0]]

    print(y_pred_future.iloc[:,1].to_list())
    return y_pred_future
