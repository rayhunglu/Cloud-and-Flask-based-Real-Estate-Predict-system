from flask import Flask, request, jsonify
import json
import pickle
import pandas as pd
import numpy as np
import predict
import datetime
app = Flask(__name__)

date=str(datetime.datetime.now()).split(' ')[0]

@app.route('/api',methods=['GET'])
def predict1():
    # Get the data from the POST request.
	# data = request.get_json(force=True)
	# predict = model.predict(data['feature'])
	# return jsonify(predict[0].tolist())
	print('hello')

@app.route('/api/recent',methods=['GET'])
def predict():
    # Get the data from the POST request.
    # data = request.get_json(force=True)
    # predict = model.predict(data['feature'])
    # return jsonify(predict[0].tolist())
    print('hello')
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')