#!/usr/bin/python3
# coding: utf8


from datetime import date

from flask import (Flask, url_for, render_template,  make_response,
                   redirect, request, g, session, Response, jsonify)

#from src.main import predict_stock
import yfinance as yf
import pandas as pd

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

data_path = 'data/'

def fetch_cryptocurrency(crypto_sel, currency_sel):
    crypto = pd.read_csv(data_path+'cryptocurrencies.csv')['Cryptocurrency'].to_list()

    currency = ['USD', 'CAD', 'EUR']

    crypto_json = []
    currency_json = []

    for i in range(len(crypto)):
        if crypto[i] == crypto_sel:
            crypto_json.append({'crypto':crypto[i], 'selected': True})
        else:
            crypto_json.append({'crypto':crypto[i], 'selected': False})

    for j in range(len(currency)):
        if currency[j] == currency_sel:
            currency_json.append({'currency':currency[j], 'selected': True})
        else:
            currency_json.append({'currency':currency[j], 'selected': False})

    return (crypto_json, currency_json)

@app.route('/')
def accueil():
    today = date.today()
    today_date = today.strftime("%B %d, %Y")

    if('cryptocurrency' in request.args):
        cryptocurrency = request.args['cryptocurrency']
        crypto_sel = cryptocurrency.split("-")[0]
        currency_sel = cryptocurrency.split("-")[1]
    else:
        crypto_sel = "BAT"
        currency_sel = "CAD"

    (crypto_json, currency_json) = fetch_cryptocurrency(crypto_sel, currency_sel)

    return render_template("accueil.html", date=today_date, crypto=crypto_json, currency=currency_json)

@app.route('/load_currency', methods=['POST'])
def load_currency():

    crypto = request.form.get('crypto')
    currency = request.form.get('currency')

    cryptocurrency = crypto + "-" + currency
    msft = yf.Ticker(cryptocurrency)

    data_file_path = data_path + cryptocurrency + '.csv'

    max_range_batcad = msft.history(period="max")
    max_range_batcad.to_csv(data_file_path, index = False)
    
    return redirect(url_for('accueil', cryptocurrency=cryptocurrency))


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