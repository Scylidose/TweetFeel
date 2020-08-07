#!/usr/bin/python3

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt 

import pickle
import tweepy

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer


from textblob import TextBlob
from wordcloud import WordCloud

import nltk
from nltk.probability import FreqDist

from sklearn.naive_bayes import MultinomialNB

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report,accuracy_score


def load_data(data_path):
    data = data = pd.read_csv(data_path + "1600000.processed.noemoticon.csv", encoding='latin-1').iloc[:, [0,5]]

    return data

def clean_tweet(tweet):
    
    excluded_punct = [".", ",", ":", "^", ";", "#"]
    
    tweet_list = tweet.split()
    clean_tokens = [re.sub('@[\w]+','',t) for t in tweet_list if re.match(r'[^\d]*$', t)]
    clean_s = ' '.join(clean_tokens)
    clean_url = re.sub(r'http\S+', '', clean_s)

    clean_punctuation = re.sub('(?<! )(?=[.,#!?()])|(?<=[.,#!?()])(?! )', ' ', clean_url)
    clean_mess = [word.lower() for word in clean_punctuation.split() if word.lower() not in stopwords.words('english') and word not in  excluded_punct]

    return clean_mess

def normalization(tweet_list):
    lem = WordNetLemmatizer()
    normalized_tweet = []
    for word in tweet_list:
        normalized_text = lem.lemmatize(word,'v')
        normalized_tweet.append(normalized_text)
    return normalized_tweet

def delete_long_words(vocabulary):
    new_vocab = []
    for i in range(len(vocabulary)):
        if len(vocabulary[i]) <= 15:
            new_vocab.append(vocabulary[i])
            
    return new_vocab


def preprocess_data(tweet):
    return delete_long_words(normalization(clean_tweet(tweet)))

def get_model(data):
    
    pkl_filename = "src/model/pickle_model.pkl"

    try:

        predictions = pd.read_csv("src/results/s140_pred.csv").iloc[:, 0]
        label_test = pd.read_csv("src/results/s140_pred.csv").iloc[:, 1]

        with open(pkl_filename, 'rb') as file:
            pipeline = pickle.load(file)

    except Exception:
        msg_train, msg_test, label_train, label_test = train_test_split(data.iloc[:, 1], data.iloc[:, 0], test_size=0.2)

        pipeline = Pipeline([
        ('bow',CountVectorizer(analyzer=preprocess_data)),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB())])

        pipeline.fit(msg_train,label_train)

        with open(pkl_filename, 'wb') as file:
            pickle.dump(pipeline, file)
    
        predictions = pipeline.predict(msg_test)

        save_pred = {'Predictions': predictions, 'y_test': label_test}

        pd.DataFrame(save_pred).to_csv('src/results/s140_pred.csv', index = None)

    print(classification_report(predictions,label_test))
    print(confusion_matrix(predictions,label_test))
    print(accuracy_score(predictions,label_test))
    
    return accuracy_score(predictions,label_test), pipeline

def get_auth():
    consumer_key = "Qs13neYllWbteSFCSMCBNPPUf"
    consumer_secret = "PLgtHZmyKenCdN0UoUN8cdKjzs2VsvEIJv1jPfIHKXXVx6TNiO"

    access_token = "1140023161980968961-gvTNlDyHEFpSXjmNKWLBdneYwsVzTK"
    access_token_secret = "ENC73nuYB0HlGuNczFYG4VeLn0zAvLgWoVtA6AsTXCrhs"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return auth

def get_tweets(search, auth):
    api = tweepy.API(auth)

    search_words = search

    public_tweets = tweepy.Cursor(api.search,
              q=search_words,
              lang="en", 
              result_type='mixed').items(200)

    tweets = {'Tweets': []}

    for tweet in public_tweets:
        tweets['Tweets'].append(tweet.text)
        
    tweets_df = pd.DataFrame(data=tweets)

    return tweets_df

def predict_tweets_sent(tweets, model):
    tweets_predictions = model.predict(tweets.iloc[:,0])

    unique, counts = np.unique(tweets_predictions, return_counts=True)

    pred_counts = np.asarray((unique, counts)).T

    if pred_counts[0][0] == 4:
        percentage = (pred_counts[0][1] * 100 / len(tweets_predictions)).round(2)
    else:
        percentage = (100 - (pred_counts[0][1] * 100 / len(tweets_predictions))).round(2)

    return percentage

