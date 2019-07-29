from flask import Flask, request, jsonify
import json
import pickle
import pandas as pd
import numpy as np
from train_predict import predict
# import train_predict.predict
import datetime
app = Flask(__name__)

# date=str(datetime.datetime.now()).split(' ')[0]

@app.route('/api',methods=['GET'])
def predict1():
	# data = request.get_json(force=True)
	# predict = model.predict(data['feature'])
	# return jsonify(predict[0].tolist())
	return "<h1>Hello Flask!</h1>"

@app.route('/api/recent',methods=['GET'])
def predict():
    link='./data/predict.csv'
    result = pd.read_csv(link)
    data=result.to_dict('index')
    # Get the data from the POST request.
    # data = request.get_json(force=True)
    # predict = model.predict(data['feature'])
    # return jsonify(predict[0].tolist())
    # return "Hello"
    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)