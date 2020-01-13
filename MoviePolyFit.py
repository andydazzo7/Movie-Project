#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:37:25 2020

@author: dshenker
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures


os.chdir("/Users/dshenker/Desktop")
df_movies = pd.read_csv("MovieProjectTest2-NYC.csv", index_col = "title")
df_movies = df_movies.drop("Unnamed: 0", axis = 1)
df_movies = df_movies.dropna()
df_movies["price"] = df_movies["price"].replace("$", "")
#print(df_movies["price"])
#print(df_movies["Rating Runtime Genre"])
col_choice = ["Earnings", "IMDB rating", "percent full", "price", "time"]
df_movies_sub = df_movies[col_choice]
print(df_movies_sub.iloc[:, 0].dtype)
df_movies_sub.iloc[:, 0] = df_movies_sub.iloc[:, 0].astype(str).str.replace(r"Gross USA:", '')
df_movies_sub.iloc[:, 0] = df_movies_sub.iloc[:, 0].str.replace(r"$", '')
df_movies_sub.iloc[:, 0] = df_movies_sub.iloc[:, 0].str.replace(r" ", '')
df_movies_sub.iloc[:, 0] = df_movies_sub.iloc[:, 0].astype(str).str.replace(r",", '').astype(float)
df_movies_sub.iloc[:, 3] = df_movies_sub.iloc[:, 3].str.replace(r"$", '').astype(float)
time_entries = np.array(df_movies["time"])

ending = np.array([x[-1:] for x in time_entries.astype(str)])
morning_times = list(np.transpose(np.where(ending == 'a')))
evening_times = list(np.transpose(np.where(ending == 'p')))

#df_movies_sub.iloc[:, 4] = df_movies_sub.iloc[:, 4].astype(str).str.replace(r'p', '')
#df_movies_sub.iloc[:, 4] = df_movies_sub.iloc[:, 4].astype(str).str.replace(r'a', '')
for i,time in enumerate(df_movies_sub.iloc[:, 4]):
    hour_in_minutes = 0
    minute = 0
    colon_index = time.find(':')
    hour = (int)(time[0:colon_index])
    minute = (int)(time[colon_index + 1:-1])
    if hour != 12:
        hour_in_minutes = hour * 60;
    if evening_times.count(i) > 0: 
        hour_in_minutes = hour_in_minutes + 720
    minute_total = hour_in_minutes + minute
    time = minute_total
    df_movies_sub.iloc[i,4] = time

df_scaled = df_movies_sub.copy()
cols = list(range(0, df_scaled.shape[1]))
for i in cols:
    if i != 2:
        mean = df_scaled.iloc[:,i].mean()
        maximum = df_scaled.iloc[:,i].max()
        minimum = df_scaled.iloc[:,i].min()
        s = maximum - minimum
        df_scaled.iloc[:,i] = (df_scaled.iloc[:,i] - mean) / s

features = ["Earnings", "IMDB rating", "price", "time"]
output = ["percent full"]
X = df_scaled[features]
y = df_scaled[output]
X.to_csv("features.csv")
y.to_csv("percents.csv")
polynomial_features= PolynomialFeatures(degree=2)
X_poly = polynomial_features.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)
y_poly_pred = model.predict(X_poly)

rmse = np.sqrt(mean_squared_error(y,y_poly_pred))
r2 = r2_score(y,y_poly_pred)
print(rmse)
print(r2)


