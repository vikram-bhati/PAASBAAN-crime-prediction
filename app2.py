import os, sys, shutil, time

from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import urllib.request
import json
from geopy.geocoders import Nominatim


endpoint='https://maps.googleapis.com/maps/api/geocode/json?address='
key='AIzaSyDM8KzL_AFUOA9lfK7ZAFCo3I74k63jG24'

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    rfc = joblib.load('model/rf_model')
    print('model loaded')

    if request.method == 'POST':

        address = request.form['Location']
        geolocator = Nominatim()
        location = geolocator.geocode(address)
        print(location.address)
        lat=[location.latitude]
        log=[location.longitude]
        latlong=pd.DataFrame({'latitude':lat,'longitude':log})
        print(latlong)

        DT= request.form['timestamp']
        latlong['timestamp']=DT
        data=latlong
        my_prediction = rfc.predict(data)

    return render_template('result.html', prediction = my_prediction)
if __name__ == '__main__':
    app.run(debug = True)
