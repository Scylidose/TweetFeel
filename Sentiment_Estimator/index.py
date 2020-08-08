#!/usr/bin/python3
# coding: utf8


import numpy as np
import pandas as pd

from datetime import date

from flask import (Flask, url_for, render_template,  make_response,
                   redirect, request, g, session, Response, jsonify)

import src.main as main

import matplotlib.pyplot as plt
from wordcloud import WordCloud

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

data_path = 'data/'

auth = main.get_auth()

@app.route('/', methods=['GET', 'POST'])
def accueil():
    search = request.form.get('search')

    percentage = None

    tweets_example = None

    #search = None
    
    data = main.load_data(data_path)
    accuracy, model = main.get_model(data)
    accuracy = round(accuracy*100,3)

    if search:
        tweets, tweets_example = main.get_tweets(search, auth)

        percentage = main.predict_tweets_sent(tweets, model)

        process_tweet = tweets.iloc[:, 0].apply(main.preprocess_data)

        plt.figure()
        happy_ratio = (percentage * len(tweets) / 100)
        plt.bar([0, 1], [happy_ratio, len(tweets) - happy_ratio], color=("g", "r"))
        plt.xticks([0, 1], ('Positive', 'Negative'))
        plt.title("Bar Plot of Positive and Negative Tweets ratio")
        plt.savefig('static/img/bar_count.png', transparent=True)

        plt.figure()
        concat_pro_words = process_tweet.str.join(" ").to_list()
        allWords = ' '.join([twts for twts in concat_pro_words])
        wordCloud = WordCloud(width=500, height=300, colormap="Blues", max_font_size=100).generate(allWords)

        plt.imshow(wordCloud, interpolation="bilinear")
        plt.axis('off')
        plt.savefig('static/img/word_cloud.png', transparent=True)


    tokens = [inner for outer in process_tweet.to_list() for inner in outer]

    common_bigrams = main.get_common_bigrams(tokens)
    return render_template("accueil.html", accuracy=accuracy, percentage=percentage,
                                         search=search, examples=tweets_example, bigrams=common_bigrams)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

