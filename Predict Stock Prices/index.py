#!/usr/bin/python3
# coding: utf8


from datetime import date

from flask import (Flask, url_for, render_template,  make_response,
                   redirect, request, g, session, Response, jsonify)

import src.main as main
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

    cryptocurrency = "BAT-CAD"

    if('cryptocurrency' in request.args):
        cryptocurrency = request.args['cryptocurrency']
        crypto_sel = cryptocurrency.split("-")[0]
        currency_sel = cryptocurrency.split("-")[1]
    else:
        crypto_sel = "BAT"
        currency_sel = "CAD"

    curr = yf.Ticker(cryptocurrency)
    
    main.fetch_currency(data_path, cryptocurrency)

    data = main.load_data(data_path + cryptocurrency + '.csv').iloc[-30:,].reset_index(drop=True)

    plt.figure()

    plt.plot(data.iloc[:,0], '-b')
    plt.plot(data.iloc[:,3], '-r')
    plt.legend(["Open Value", "Close Value"])
    plt.title("Open and close for " + crypto_sel + " price per day (Last 30 Days) ")
    plt.xticks([])

    plt.savefig('static/img/open_close.png', transparent=True)

    plt.figure()
    plt.plot(data.iloc[:,1], '-c')
    plt.plot(data.iloc[:,2], '-m')
    plt.legend(["Highest", "Lowest"])
    plt.title("Highest and Lowest for " + crypto_sel + " price per day (Last 30 Days)")
    plt.xticks([])

    plt.savefig('static/img/high_low.png', transparent=True)
    
    plt.figure()
    plt.plot(data.iloc[:,4])
    plt.title("Volume value for " + crypto_sel + " per day (Last 30 Days)")
    plt.xticks([])

    plt.savefig('static/img/volume.png', transparent=True)

    (crypto_json, currency_json) = fetch_cryptocurrency(crypto_sel, currency_sel)
    print("-------------------> ", data.iloc[:, -1])

    prediction = 0

    return render_template("accueil.html", 
                            date=today_date, crypto=crypto_json, currency=currency_json, 
                            desc=curr.info['description'], 
                            open = data.iloc[-1, 0], close=prediction,
                            open_close ='/static/img/open_close.png', high_low='/static/img/high_low.png', volume='/static/img/volume.png',
                            year_accuracy='/static/img/year_accuracy.png')

@app.route('/load_currency', methods=['POST'])
def load_currency():

    crypto = request.form.get('crypto')
    currency = request.form.get('currency')

    cryptocurrency = crypto + "-" + currency
    curr = yf.Ticker(cryptocurrency)
    
    data_file_path = data_path + cryptocurrency + '.csv'

    max_range_curr = curr.history(period="max")
    max_range_curr.to_csv(data_file_path, index = False)
    
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


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response