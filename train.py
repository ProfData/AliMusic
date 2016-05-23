#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import pandas as pd
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
