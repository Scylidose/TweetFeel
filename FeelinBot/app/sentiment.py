import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from wordcloud import WordCloud

import firebase

import requests
import json
import math

app = Flask(__name__)

def clean_inputs(inputs):
    
    excluded_punct = [".", ",", ":", "^", ";", "#", "-", "_"]
    
    inputs_list = inputs.split()
    clean_tokens = [re.sub('@[\w]+','',t) for t in inputs_list if re.match(r'[^\d]*$', t)]
    clean_s = ' '.join(clean_tokens)
    clean_url = re.sub(r'http\S+', '', clean_s)

    clean_punctuation = re.sub('(?<! )(?=[-.,#!?()_])|(?<=[-.,#!?()_])(?! )', ' ', clean_url)
    clean_mess = [word.lower() for word in clean_punctuation.split() if word.lower() not in stopwords.words('english') and word not in  excluded_punct]

    return clean_mess

def normalization(inputs_list):
    lem = WordNetLemmatizer()
    normalized_inputs = []
    for word in inputs_list:
        normalized_text = lem.lemmatize(word,'v')
        normalized_inputs.append(normalized_text)
    return normalized_inputs

def preprocess_data(inputs):
    return normalization(clean_tweet(inputs))