#!/usr/bin/python3
# coding: utf8


import datetime
from flask import (Flask, url_for, render_template,  make_response,
                   redirect, request, g, session, Response, jsonify)

#from src.main import predict_stock

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def accueil():
    return render_template("accueil.html")


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