#!/usr/bin/python3
# coding: utf8


import datetime
from flask import (Flask, url_for, render_template,  make_response,
                   redirect, request, g, session, Response, jsonify)

#from src.main import predict_stock
import yfinance as yf
import pandas as pd

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

data_path = 'data/'

@app.route('/')
def accueil():
    crypto = pd.read_csv(data_path+'cryptocurrencies.csv')['Cryptocurrency'].to_list()

    currency = ['USD', 'CAD', 'EUR']

    print(crypto)

    return render_template("accueil.html")

@app.route('/load_currency', methods=['POST'])
def load_currency():

    currency = request.form["currency"]

    msft = yf.Ticker(currency)

    data_file_path = data_path + currency + '.csv'

    max_range_batcad = msft.history(period="max")
    max_range_batcad.to_csv(data_file_path, index = False)


'''
@app.route('/predict_stock', methods=['POST'])
def predict_stock():

    (unscaled_y_pred, unscaled_y_test) = predict_stock()

    print("Test Target\n")
    print(unscaled_y_test[:10])
    print("\n----------------\n")
    print("Predict Target\n")
    print(unscaled_y_pred[:10])


    plt.gcf().set_size_inches(20, 10, forward=True)

    real_close = plt.plot(unscaled_y_test[:,0], label='Real Close Value')
    pred_close = plt.plot(unscaled_y_pred[:,0], label='Predicted Close Value')

    plt.legend(['Real Close Value', 'Predicted Close Value'])

    plt.show()
    return True
'''