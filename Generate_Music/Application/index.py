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

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
CORS(app)


@app.route('/')
def accueil():
    battle_song_dir = "ost/battle/"
    buildings_song_dir = "ost/buildings/"
    route_song_dir = "ost/route/"

    train_battle = get_songs(battle_song_dir)
    train_buildings = get_songs(buildings_song_dir)
    train_route = get_songs(route_song_dir)

    result_battle_song_dir = "result/battle/"
    result_buildings_song_dir = "result/buildings/"
    result_route_song_dir = "result/route/"

    result_battle = get_songs(result_battle_song_dir)
    result_buildings = get_songs(result_buildings_song_dir)
    result_route = get_songs(result_route_song_dir)

    # return render_template("accueil.html", train=train, result=result, model=model, info=info)
    return render_template("accueil.html", 
                           url_train_battle=train_battle, title_train_battle=clean_songs_path(train_battle),
                           url_train_buildings=train_buildings, title_train_buildings=clean_songs_path(train_buildings),
                           url_train_route=train_route, title_train_route=clean_songs_path(train_route),
                           result_battle=result_battle,
                           result_buildings=result_buildings,
                           result_route=result_route)

def get_songs(song_dir):
    train = []
    for file in glob.glob("./static/"+song_dir+"*.midi"):

        file_name = "/".join(file.split("/")[2:])
        file_name = file_name.replace('\\', '/')

        file_name = file_name.replace("/static/", "")

        train.append(file_name)
    print(train)
    return train

def clean_songs_path(songs_path):
    new_songs_path = []

    for file in songs_path:
        file = file.split("/")[-1]
        file = file.replace("_", " ")
        file = file.replace(".midi", "")
        new_songs_path.append(file)

    return new_songs_path

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response