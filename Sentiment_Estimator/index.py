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

auth = main.get_auth()

@app.route('/', methods=['GET', 'POST'])
def accueil():
    search = request.form.get('search')

    percentage = None
    accuracy = None

    if search:
        data = main.load_data(data_path)
        accuracy, model = main.get_model(data)

        tweets = main.get_tweets(search, auth)

        percentage = main.predict_tweets_sent(tweets, model)

    return render_template("accueil.html", accuracy=accuracy, percentage=percentage, search=search)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response