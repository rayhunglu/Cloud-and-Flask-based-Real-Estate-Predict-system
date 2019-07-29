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
import datetime
class crawler:
    def __init__(self):
        self.date=str(datetime.datetime.now()).split(' ')[0]
    def get_headers(self):
        # Creating headers.
        headers = {
    #         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #                'accept-encoding': 'gzip, deflate, sdch, br',
    #                'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
                   'cache-control': 'max-age=0',
    #                'upgrade-insecure-requests': '1',
                   'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
        return headers
    def clean(self,text):
        if text:
            return ' '.join(' '.join(text).split())
        return None
    def get_data_from_json(self,raw_json_data):
        # getting data from json (type 2 of their A/B testing page)
        try:
            cleaned_data = clean(raw_json_data).replace('<!--', "").replace("-->", "")
        except ValueError:
            a=None
        properties_list = []

        try:
            json_data = json.loads(cleaned_data)
            search_results = json_data.get('searchResults').get('listResults', [])

            for properties in search_results:
                address = properties.get('addressWithZip')
                property_info = properties.get('hdpData', {}).get('homeInfo')
                postal_code = property_info.get('zipcode')
                price=property_info.get('price')
                bedrooms = properties.get('beds')
                bathrooms = properties.get('baths')
                area = properties.get('area')
                latitude=properties.get('latLong').get('latitude')
                longitude=properties.get('latLong').get('longitude')
                property_url = properties.get('detailUrl')
                title = properties.get('statusText')

                data = {'address': address,
                        'postal_code': postal_code,
                        'price': price,
                        'dateSold':dateSold,
                        'yearBuilt':yearBuilt,
                        'lotSize':lotSize,
                        'homeType':homeType,
                        'rentZestimate':rentZestimate,
                        'taxAssessedValue':taxAssessedValue,
                        'bedrooms':bedrooms,
                        'bathrooms':bathrooms,
                        'area':area,
                        'latitude':latitude,
                        'longitude':longitude,
                        'url': property_url,
                        'title': title}
                properties_list.append(data)
            return properties_list

        except ValueError:
            print("Invalid json")
            return None
    def get_data_from_html(self,response,search_results):
        properties_lan_lon_list=self.get_lan_lon_info(response)
        properties_list = []
        for properties in search_results:
            try:
                raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
                raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
                raw_state = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
                raw_postal_code = properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
                raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
                raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
                url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")

                address = self.clean(raw_address)
                city = self.clean(raw_city)
                state = self.clean(raw_state)
                postal_code = self.clean(raw_postal_code)
                price = raw_price[0].replace(',','').split('$')[1]
                info = self.clean(raw_info).replace(u"\xb7", ',')
                property_url = "https://www.zillow.com" + url[0] if url else None
                
                properties = {'crawler date':self.date
                              ,'address': raw_address[0]+','+raw_city[0]+','+raw_state[0]
                              ,'postal_code': postal_code
                              ,'url': property_url
                              ,'bedrooms':info.replace(' ','').split('bd')[0]
                              ,'bathrooms':info.replace(' ','').split(',')[1].split('ba')[0]
                              ,'area':info.replace(' ','').replace(',','').split('ba')[1].split('s')[0]
                              ,'latitude':''
                              ,'longitude':''
                              ,'price': price
                             }
                properties_list.append(properties)
            except:
                continue
        properties_list=self.combine(properties_list,properties_lan_lon_list)
        return (properties_list)
    def get_page_url(url,page):
        if page==1:
            return url
        else:
            return url+str(page)+'_p/'

    def write_data_to_csv(self,data,name):
        # saving scraped data to csv.
        keys = data[0].keys()
        path='./data/'+name+'.csv'
        if os.path.exists(path):
            with open(path, 'a') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writerows(data)
        else:
            with open(path, 'a') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
    # def save_to_file(self,response):
    #     # saving response to `response.html`
    #     with open("response.html", 'w') as fp:
    #         fp.write(response.text)
    def get_lan_lon_info(self,response):
        k=response.text
        properties_lan_lon_list=[]
        c=k.split('search-results')[1].split('article data-unmappable')
        c.pop(0)
        for i in c:
            soup = BeautifulSoup(i)
            dic={}
            dic['latitude']=soup(itemprop="latitude")[0]['content']
            dic['longitude']=soup(itemprop="longitude")[0]['content']
            properties_lan_lon_list.append(dic)
        return properties_lan_lon_list
    def combine(self,properties_list,properties_lan_lon_list):
        for i in range(len(properties_list)):
            for j in properties_lan_lon_list[i]:
                properties_list[i][j]=properties_lan_lon_list[i][j]
        return properties_list
    # def df_to_csv(name,df):
    #     export_csv = df.to_csv (r'./new_train_df.csv', index = None, header=True)
        