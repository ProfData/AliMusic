#!/usr/bin/env python

import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta


users = pd.read_csv(filepath_or_buffer="/home/frankfzw/Ali/users.csv", names=['user_id', 'song_id', 'gmt_create', 'action_type', 'ds'])
songs = pd.read_csv(filepath_or_buffer='/home/frankfzw/Ali/songs.csv', names=['song_id', 'artist_id', 'publish_time', 'song_init_plays', 'language', 'gender'])


def main():
    print "Ali Demo"
    usersLen = len(users.index)
    songsLen = len(songs.index)
    print 'User Record Size: {}'.format(len(users.index))
    print 'Songs Number: {}'.format(len(songs.index))
    startTimeStr = users.loc[usersLen -1, 'ds']
    endTimeStr = users.loc[0, 'ds']
    startTime = datetime.strptime(str(startTimeStr), '%Y%m%d')
    endTime = datetime.strptime(str(endTimeStr), '%Y%m%d')

    #create an empty table to store play count of song by date
    songIdList = songs['song_id'].values
    # dateList = users['ds'].values
    # temp = [songIdList, dateList]
    # tuples = list(itertools.product(*temp))
    columns = ['count']
    index = pd.Index(songIdList)
    index.name = 'song_id'
    # result = pd.DataFrame(index=indexs, columns=columns)
    # result = result.fillna(0)

    #update the result table
    print 'Date from {} to {}'.format(startTimeStr, endTimeStr)
    delta = (endTime - startTime).days
    # create a dateframe with date, artist_id and play count
    for day in range(0, delta):
        currentDate = datetime.strftime((startTime + timedelta(day)), "%Y%m%d")
        intDate = int(currentDate)
        currentUsers = users.query('ds == [intDate]')
        record = [None] * len(songIdList)
        for i in range(0, len(songIdList)):
            record[i] = currentUsers[currentUsers['song_id'] == songIdList[i]].shape[0]
        
        # create one-day play record
        recordDF = pd.DataFrame(data=record, index=index, columns=columns)
        recordDF
        recordDF.to_csv('{}.csv'.format(currentDate))


    #print songs.song_id




if __name__ == "__main__":
    main()
