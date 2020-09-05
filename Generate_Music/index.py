#!/usr/bin/python3
# coding: utf8


import numpy as np
import pandas as pd

from datetime import date

from flask import (Flask, url_for, render_template,  make_response,
                   redirect, request, g, session, Response, jsonify)

#import Python.main as main
import time

template_dir = "Application/templates"
app = Flask(__name__, template_folder=template_dir)

app.config['JSON_SORT_KEYS'] = False

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response