#!/usr/bin/env python

import numpy as np
import os
import pandas as pd
from datetime import datetime
from datetime import timedelta


file_prefix = '/home/frankfzw/Ali'


raw_users = pd.read_csv(filepath_or_buffer="{}/mars_tianchi_user_actions.csv".format(file_prefix), names=['user_id', 'song_id', 'gmt_create', 'action_type', 'ds'])
songs = pd.read_csv(filepath_or_buffer='{}/mars_tianchi_songs.csv'.format(file_prefix), names=['song_id', 'artist_id', 'publish_time', 'song_init_plays', 'language', 'gender'])


def main():
    print "Ali Demo"
    usersLen = len(raw_users.index)
    songsLen = len(songs.index)
    print 'User Record Size: {}'.format(usersLen)
    print 'Songs Number: {}'.format(songsLen)
    users = raw_users.sort(['ds'])
    days = set(users['ds'].values)
    startTimeStr = days[0]
    endTimeStr = days[len(days) - 1]
    startTime = datetime.strptime(str(startTimeStr), '%Y%m%d')
    endTime = datetime.strptime(str(endTimeStr), '%Y%m%d')

    #create an empty table to store play count of song by date
    songIdList = songs['song_id'].values
    #delete the duplicate artist_id
    artistIdList = list(set(songs['artist_id'].values))

    # dateList = users['ds'].values
    # temp = [songIdList, dateList]
    # tuples = list(itertools.product(*temp))
    columns = ['song_id', 'count']
    artistColumns = ['artist_id', 'count']
    # result = pd.DataFrame(index=indexs, columns=columns)
    # result = result.fillna(0)

    artistDailyRecord = {}
    #update the result table
    print 'Date from {} to {}'.format(startTimeStr, endTimeStr)
    delta = (endTime - startTime).days
    # create a dateframe with date, artist_id and play count
    for day in days:
    #for day in range(0, 1):
        print 'Processing day {}'.format(day)
        intDate = int(day)
        currentUsers = users.query('ds == [intDate]')
        record = [None] * len(songIdList)
        for i in range(0, len(songIdList)):
            record[i] = currentUsers[currentUsers['song_id'] == songIdList[i]].shape[0]
        
        # create daily play record
        recordDF = pd.DataFrame(data=zip(songIdList, record), columns=columns)

        # create daily play counts of a artist
        artistRecord = [None] * len(artistIdList)
        for i in range(0, len(artistIdList)):
        #for i in range(0, 1):
            artist = artistIdList[i]
            belongingSongs = songs[songs['artist_id'] == artist]
            res = pd.merge(belongingSongs, recordDF, on='song_id', how='inner')
            count = reduce(lambda x, y: x + y, res['count'].values)
            artistRecord[i] = count
            dateArry = [day] * belongingSongs.shape[0]
            index = [0] * belongingSongs.shape[0]
            for j in range(0, belongingSongs.shape[0]):
                index[j] = day * belongingSongs.shape[0] + j

            artistDailyDF = pd.DataFrame(index=index, data=zip(res['song_id'].values, res['count'].values), columns=['song_id', 'count'])
            artistDailyDF.insert(0, 'ds', dateArry)
            if artist in artistDailyRecord:
                artistDailyRecord[artist] = pd.concat([artistDailyRecord[artist], artistDailyDF])
            else:
                artistDailyRecord[artist] = artistDailyDF


        artistRecordDF = pd.DataFrame(data=zip(artistIdList, artistRecord), columns=artistColumns)
        artistRecordDF.to_csv('{}/demo/data/{}_artist.csv'.format(file_prefix, day))
        # artistRecordDF.to_csv(os.path.join(file_prefix, '{}_artist.csv'.format(currentDate)))
        recordDF.to_csv('{}/demo/data/{}.csv'.format(file_prefix, day))
        # recordDF.to_csv(os.path.join(file_prefix, '{}.csv'.format(currentDate)))


    for artist in artistIdList:
        artistDailyRecord[artist].to_csv('{}/demo/data/{}.csv'.format(file_prefix, artist))
        # artistDailyRecord[artist].to_csv(os.path.join(file_prefix, '{}.csv'.format(artist)))
    #print songs.song_id




if __name__ == "__main__":
    main()
