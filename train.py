#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.pipeline import Pipeline
from datetime import datetime
from datetime import timedelta
from sklearn.metrics import mean_squared_error

import math

# read data from csv

file_prefix = '/home/frankfzw/Ali'

startTimeStr = '20150301'
endTimeStr = '20150830'
startTime = datetime.strptime(str(startTimeStr), '%Y%m%d')
endTime = datetime.strptime(str(endTimeStr), '%Y%m%d')
delta = (endTime - startTime).days

songs = pd.read_csv(filepath_or_buffer='{}/mars_tianchi_songs.csv'.format(file_prefix), names=['song_id', 'artist_id', 'publish_time', 'song_init_plays', 'language', 'gender'])
artists = list(set(songs['artist_id'].values))



# for day in range(0, delta + 1):
#     currentDate = datetime.strftime((startTime + timedelta(day)), "%Y%m%d")
#     record = pd.read_csv(filepath_or_buffer="/home/frankfzw/Ali/demo/{}.csv".format(currentDate))
#     playRecord[currentDate] = record
#
# songList = playRecord.get(currentDate)['song_id'].values
#
# #train one song
# i = 0
# for song in songList:
#     counts = map(lambda x: x[x['song_id'] == song].iloc[0, 2], playRecord.values())
#     print "song id: {}; counts {}".format(song, counts)

# print songList

def cost_function(ground_true, prediction):
    
    tmp = map(lambda x, y: pow(((float(x) - float(y)) / float(y)), 2), prediction, ground_true)
    return pow(sum(tmp)/len(tmp), 0.5)


model_dict = dict()


for artist in artists:
    records = pd.read_csv(filepath_or_buffer='{}/demo/data/{}.csv'.format(file_prefix, artist))
    first_day = records[records['ds'] == int(startTimeStr)]
    belonging_songs = list(set(first_day['song_id'].values))
    print 'Processing {} with {} songs'.format(artist, len(belonging_songs))
    daily_count = records.groupby('ds')['count'].sum()
    days = list(daily_count.index)

    inputs_x = map(lambda x: (datetime.strptime(str(x), "%Y%m%d") - startTime).days, list(days))
    # train the model with single song_id
    train_part = int(len(inputs_x) * 0.7)
    for song in belonging_songs:
        daily = records[records['song_id'] == song]
        inputs_y = list(daily['count'].values)
        x_plot = np.asarray(inputs_x)
        y_plot = np.asarray(inputs_y)
        # X_predict = x_plot[:, np.newaxis]
        X = x_plot[:train_part][:, np.newaxis]
        Y = y_plot[:train_part]
        X_validate = x_plot[train_part:][:, np.newaxis]
        Y_validate = y_plot[train_part:]
        # plt.scatter(X, Y, label="trainning points")
        # plt.scatter(X_validate, Y_validate, label='validate points', marker='v')
        tmp = []
        for degree in [1, 2, 3, 4, 5]:
            # for alpha in np.linspace(1, 5, 10):
            ridge = linear_model.Ridge()
            lasso = linear_model.Lasso(alpha=0.1)
            # bayes = linear_model.BayesianRidge()
            model = Pipeline([('poly', PolynomialFeatures(degree=degree)), ('linear', ridge)])
            model.fit(X, Y)
            y_pred = model.predict(X_validate)
            score = mean_squared_error(Y_validate, y_pred)
            tmp.append((degree, score, model))
            # y_pre = model.predict(x_plot[:, np.newaxis])
            # plt.plot(x_plot, y_pre, label="degree {}".format(degree))
        tmp.sort(key=lambda tup: tup[1])
        # print "Song {} of Artist {}: model degree {}, score {}".format(song, artist, tmp[0][0], tmp[0][1])
        model_dict[song] = tmp[0][2]
        # plt.legend(loc="lower left")
        # plt.show()

    # predict
    count = [0] * len(X_validate)
    for song in belonging_songs:
        song_count = model_dict[song].predict(X_validate)
        count = map(lambda x, y: x + y, count, song_count)
    
    delta = len(inputs_x) - train_part
    a = list(daily_count.values)[train_part - delta:train_part]
    real_count = list(daily_count.values)[train_part:]
    score = cost_function(real_count, a)
    print "Artist {}: predict score {}".format(artist, score)

    # inputs = records[['ds', 'song_id']].values
    # values = records[['count']].values
    # train_size = len(inputs) * 0.8
    # inputs_train = inputs[:train_size]
    # inputs_test = inputs[train_size:]
    # values_train = values[:train_size]
    # values_test = values[train_size:]
    # plot the original data
    # colors = cm.rainbow(np.linspace(0, 1, len(belonging_songs)))
    # for song, c in zip(belonging_songs, colors):
    #     song_records = records[records['song_id'] == song][['ds', 'count']]
    #     ds = map(lambda x: (datetime.strptime(str(x), '%Y%m%d') - startTime).days, song_records['ds'].values.T)
    #     count = song_records['count'].values.T
    #     plt.scatter(ds, count, color=c)
    #     plt.plot(ds, count, color=c)
    # plt.xlabel("date")
    # plt.ylabel("count")
    # plt.show()

