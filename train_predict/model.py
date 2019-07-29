import pandas as pd
import numpy as np
import random as rnd
import pickle
import csv
# machine learning
from sklearn.linear_model import LinearRegression

link='../data/train.csv'
train_df = pd.read_csv(link)

train_df['bedrooms'] = train_df['bedrooms'].fillna(0)
train_df['bathrooms'] = train_df['bathrooms'].fillna(0)
train_df=train_df.drop(['id','address','url'], axis=1)

data=train_df.drop(["price"], axis=1).values
target=train_df["price"].values
model_train_list=[1000,2000,5000]

for i in model_train_list:
    X_train=data[:i]
    y_train=target[:i]
    logreg = LinearRegression()
    logreg.fit(X_train, y_train)
    # save the model to disk
    filename = 'model_'+str(i)+'.pkl'
    with open('../trained_model/'+filename, 'wb') as file:
        pickle.dump(logreg, file)

