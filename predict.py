import crawler
import requests
import urllib.request as urlrequest
from lxml import html
import sys
import pickle
import numpy as np
import pandas as pd
import json
from bs4 import BeautifulSoup
import csv
import time
import os.path

url='https://www.zillow.com/homes/for_sale/San-Jose-CA_rb/days_sort/'
crawl=crawler.crawler()
response =requests.post(url,headers=crawl.get_headers())
crawl.save_to_file(response)
parser = html.fromstring(response.text)
search_results = parser.xpath("//div[@id='search-results']//article")
properties_list=[]
if not search_results:
    raw_json_data = parser.xpath('//script[@data-zrr-shared-data-key="mobileSearchPageStore"]//text()')
    properties_list=crawl.get_data_from_json(raw_json_data)
else:
    properties_list=crawl.get_data_from_html(response,search_results)

crawl.write_data_to_csv(properties_list,'predict')

#
link='./data/predict.csv'
test_df = pd.read_csv(link)
X_test=test_df.drop(['crawler date','address','url','price'], axis=1)
Y_test=test_df['price']
model_train_list=[1000,2000,5000]
# Load trained model from file
for i in model_train_list:
    filename = 'model_'+str(i)+'.pkl'
    with open('./trained_model/'+filename, 'rb') as file:
        model = pickle.load(file)

    result=model.predict(X_test)
    test_df['model_'+str(i)]=result

export_csv = test_df.to_csv (r'./predict_result.csv', index = None, header=True)