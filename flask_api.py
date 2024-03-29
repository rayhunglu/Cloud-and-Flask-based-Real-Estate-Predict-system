from flask import Flask, request, jsonify
import json
import pickle
import pandas as pd
import numpy as np
from model import predict
# import train_predict.predict
import datetime
app = Flask(__name__)

# date=str(datetime.datetime.now()).split(' ')[0]

@app.route('/api',methods=['GET'])
def predict1():
    
	return "<h1>Welcome!</h1>"

@app.route('/api/recent',methods=['GET'])
def predict():
    link='./model/data/predict.csv'
    result = pd.read_csv(link)
    data=result.to_dict('index')
    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)