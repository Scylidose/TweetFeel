#!/usr/bin/python3
# coding: utf8


import numpy as np
import pandas as pd

from datetime import date

from flask import (Flask, url_for, render_template,  make_response,
                   redirect, request, g, session, Response, jsonify)

import src.main as main

import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

data_path = 'data/'

'''
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
'''

def save_plot(data, first_data, second_data, color, legend, title, save):
    _, ax = plt.subplots()

    plt.plot(data.iloc[:, 0], data.iloc[:,first_data], color[0])
    if second_data is not None:
        plt.plot(data.iloc[:,second_data], color[1])
        plt.legend(legend)

    plt.title(title)
    plt.xticks(rotation=45)

    every_nth = 3
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    plt.savefig('static/img/'+save+'.png', transparent=True)

@app.route('/')
def accueil():
    check_pred_today = pd.read_csv("src/results/today_score.csv")

    today = date.today()
    today_date = today.strftime("%B %d, %Y")
    
    cryptocurrency = "BAT-CAD"

    main.download_data(data_path, cryptocurrency)

    data = main.load_data(data_path, cryptocurrency)

    if(check_pred_today.iloc[0, 0] != today_date):
        data.iloc[:, 0] = pd.to_datetime(data.iloc[:,0],format='%Y-%m-%d').dt.strftime('%d-%m').tolist()

        data_sel = data.iloc[-30:,].reset_index(drop=True)

        save_plot(data_sel, 1, 4, ['-b', '-r'], ["Open Value", "Close Value"],
        "Open and close for " + cryptocurrency + " price per day", "open_close")

        save_plot(data_sel, 2, 3, ['-c', '-m'], ["Highest", "Lowest"],
        "Highest and Lowest for " + cryptocurrency + " price per day", "high_low")

        print(data_sel)

        save_plot(data_sel, 5, None,['-g'], None, "Volume value for " + cryptocurrency + " per day", "volume")

        prediction_result = main.predict_stock(data_path, cryptocurrency)

        (unscaled_y_pred, unscaled_y_test, predicted_close_today) = prediction_result[0]

        accuracy = prediction_result[1]

        prediction = predicted_close_today[0]

        today_pred = {'Date': [], 'Prediction': [], 'Accuracy': []}

        today_pred['Date'] = today_date
        today_pred['Prediction'] = prediction
        today_pred['Accuracy'] = accuracy

        today_pred = pd.DataFrame(today_pred, index=[0])

        today_pred.to_csv(r'src/results/today_score.csv', index=False)


        plt.figure()
        data_sel = -len(unscaled_y_test)

        fig, ax = plt.subplots()
        plt.plot(data.iloc[data_sel:,0], unscaled_y_test[:,0], '-b', label='Real Close Value')
        plt.plot(unscaled_y_pred[:,0], '-r', label='Predicted Close Value')
        plt.legend(['Real Close Value', 'Predicted Close Value'])
        plt.title("Predicted and Real close value for " + cryptocurrency + " (Last Year)")
        plt.xticks(rotation=45)

        every_nth = 14
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        plt.savefig('static/img/year_accuracy.png', transparent=True)

    else:
        prediction = check_pred_today.iloc[0, 1]
        accuracy = check_pred_today.iloc[0, 2]

    diff = (data.iloc[-2, 4] - prediction) / data.iloc[-2, 4] * 100

    if data.iloc[-2, 4] > prediction:
        diff = -diff
    
    return render_template("accueil.html", 
                            date=today_date, 
                            accuracy=accuracy, diff=round(diff,3),
                            open = data.iloc[-1, 1], close=prediction.round(decimals=5),
                            open_close ='/static/img/open_close.png', high_low='/static/img/high_low.png', volume='/static/img/volume.png',
                            year_accuracy='/static/img/year_accuracy.png')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response