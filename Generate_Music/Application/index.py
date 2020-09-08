#!/usr/bin/python3
# coding: utf8


import numpy as np
import pandas as pd
import glob

from datetime import date

from flask import (Flask, url_for, render_template,  make_response,
                   redirect, request, g, session, Response, jsonify)
from flask_cors import CORS, cross_origin

#import Python.main as main
import time

template_dir = "templates"
app = Flask(__name__, template_folder=template_dir)

app.config['JSON_SORT_KEYS'] = False
CORS(app)

@app.route('/')
def home():
    song_dir = "midi"

    songs = []

    for file in glob.glob(song_dir+"/*.midi"):
        songs.append(file)
    
    return {'songs': songs}

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response