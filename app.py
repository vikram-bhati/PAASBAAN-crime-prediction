import os, sys, shutil, time

from flask import Flask, request, jsonify, render_template,send_from_directory
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import urllib.request
import json
from geopy.geocoders import Nominatim



app = Flask(__name__)



@app.route('/')
def root():
    return render_template('index.html')

@app.route('/images/<Paasbaan>')
def download_file(Paasbaan):
    return send_from_directory(app.config['images'], Paasbaan)

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/work.html')
def work():
    return render_template('work.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/result.html', methods = ['POST'])
def predict():
    rfc = joblib.load('model/rf_model')
    print('model loaded')

    if request.method == 'POST':

        address = request.form['Location']
        geolocator = Nominatim()
        location = geolocator.geocode(address,timeout=None)
        print(location.address)
        lat=[location.latitude]
        log=[location.longitude]
        latlong=pd.DataFrame({'latitude':lat,'longitude':log})
        print(latlong)

        DT= request.form['timestamp']
        latlong['timestamp']=DT
        data=latlong
        cols = data.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        data = data[cols]

        data['timestamp'] = pd.to_datetime(data['timestamp'].astype(str), errors='coerce')
        data['timestamp'] = pd.to_datetime(data['timestamp'], format = '%d/%m/%Y %H:%M:%S')
        column_1 = data.ix[:,0]
        DT=pd.DataFrame({"year": column_1.dt.year,
              "month": column_1.dt.month,
              "day": column_1.dt.day,
              "hour": column_1.dt.hour,
              "dayofyear": column_1.dt.dayofyear,
              "week": column_1.dt.week,
              "weekofyear": column_1.dt.weekofyear,
              "dayofweek": column_1.dt.dayofweek,
              "weekday": column_1.dt.weekday,
              "quarter": column_1.dt.quarter,
             })
        data=data.drop('timestamp',axis=1)
        final=pd.concat([DT,data],axis=1)
        X=final.iloc[:,[1,2,3,4,6,10,11]].values
        my_prediction = rfc.predict(X)
        if my_prediction[0][0] == 1:
            my_prediction='Predicted crime : Act 379-Robbery'
        elif my_prediction[0][1] == 1:
            my_prediction='Predicted crime : Act 13-Gambling'
        elif my_prediction[0][2] == 1:
            my_prediction='Predicted crime : Act 279-Accident'
        elif my_prediction[0][3] == 1:
            my_prediction='Predicted crime : Act 323-Violence'
        elif my_prediction[0][4] == 1:
            my_prediction='Predicted crime : Act 302-Murder'
        elif my_prediction[0][5] == 1:
            my_prediction='Predicted crime : Act 363-kidnapping'
        else:
            my_prediction='Place is safe no crime expected at that timestamp.'



    return render_template('result.html', prediction = my_prediction)


if __name__ == '__main__':
    app.run(debug = True)
