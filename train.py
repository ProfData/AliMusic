#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from datetime import datetime
from datetime import timedelta

# read data from csv

startTimeStr = '20150301'
endTimeStr = '20150315'
startTime = datetime.strptime(str(startTimeStr), '%Y%m%d')
endTime = datetime.strptime(str(endTimeStr), '%Y%m%d')
delta = (endTime - startTime).days

songs = pd.read_csv(filepath_or_buffer='/home/frankfzw/Ali/songs.csv', names=['song_id', 'artist_id', 'publish_time', 'song_init_plays', 'language', 'gender'])
artists = list(set(songs['artist_id'].values))


playRecord = dict()

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

for artist in artists:
    records = pd.read_csv(filepath_or_buffer='/home/frankfzw/Ali/demo/{}.csv'.format(artist))
    dailyDF = records[records['ds'] == int(startTimeStr)]
    belonging_songs = list(set(dailyDF['song_id'].values))
    print 'Processing {} with {} songs'.format(artist, len(belonging_songs))
    inputs = records[['ds', 'song_id']].values
    values = records[['count']].values
    train_size = len(inputs) * 0.8
    inputs_train = inputs[:train_size]
    inputs_test = inputs[train_size:]
    values_train = values[:train_size]
    values_test = values[train_size:]
    # plot the original data
    colors = cm.rainbow(np.linspace(0, 1, len(belonging_songs)))
    for song, c in zip(belonging_songs, colors):
        song_records = records[records['song_id'] == song][['ds', 'count']]
        ds = map(lambda x: (datetime.strptime(str(x), '%Y%m%d') - startTime).days, song_records['ds'].values.T)
        count = song_records['count'].values.T
        plt.scatter(ds, count, color=c)
        plt.plot(ds, count, color=c)
    plt.xlabel("date")
    plt.ylabel("count")
    plt.show()
