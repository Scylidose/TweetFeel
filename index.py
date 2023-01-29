#!/usr/bin/python3
# coding: utf8


import numpy as np
import pandas as pd

from flask import (Flask, url_for, render_template,  make_response,
                   redirect, request, g, session, Response, jsonify)

import src.main as main

import matplotlib.pyplot as plt
from wordcloud import WordCloud

import requests
import json
import math

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

data_path = 'data/'

auth = main.get_auth()

@app.route('/', methods=['GET', 'POST'])
def accueil():
    search = request.form.get('search')

    percentage = None

    tweets_example = None

    common_words = ""

    predict_tweets_random = []

    #search = None
    
    data = main.load_data(data_path)
    accuracy, model = main.get_model(data)
    accuracy = round(accuracy*100,3)

    if search:
        tweets, random_tweets = main.get_tweets(search, auth)

        percentage = main.predict_tweets_sent(tweets, model)

        process_tweet = tweets.iloc[:, 0].apply(main.preprocess_data)

        tweets_random_df = {'Tweets': []}

        tweets_example = []
        for tweet in random_tweets:
            res = requests.get("https://publish.twitter.com/oembed?url=https://twitter.com/Interior/status/"+str(tweet.id))
            res_json = json.loads(res.text)
            tweets_example.append(res_json['html'])

            tweets_random_df['Tweets'].append(tweet.text)
    
        tweets_random_df = pd.DataFrame(data=tweets_random_df)

        predict_tweets_random = model.predict(tweets_random_df.iloc[:, 0])


        happy_ratio = (percentage * len(tweets) / 100)
        ratio = [math.trunc(happy_ratio), math.trunc(len(tweets) - happy_ratio)]

        plt.figure()   

        plt.bar([0, 1], [ratio[0], ratio[1]], color=("g", "r"))
        plt.xticks([0, 1], ('Positive', 'Negative'))
        plt.title("Bar Plot of Positive and Negative Tweets ratio")

        plt.savefig('static/img/bar_count.png', transparent=True,)

        plt.figure()
        concat_pro_words = process_tweet.str.join(" ").to_list()
        allWords = ' '.join([twts for twts in concat_pro_words])
        wordCloud = WordCloud(width=500, height=300, colormap="Blues", max_font_size=100).generate(allWords)

        plt.imshow(wordCloud, interpolation="bilinear")
        plt.axis('off')
        plt.savefig('static/img/word_cloud.png', transparent=True)


        vocabulary = [inner for outer in process_tweet.to_list() for inner in outer]

        common_words = main.get_common_words(vocabulary)
    
    return render_template("accueil.html", accuracy=accuracy, percentage=percentage,
                                         search=search, examples=tweets_example, random_pred=predict_tweets_random,
                                         common_words=common_words)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

