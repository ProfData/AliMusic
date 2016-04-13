#!/usr/bin/env/ python

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import pandas as pd
from datetime import datetime
from datetime import timedelta

# read data from csv

startTimeStr = '20150301'
endTimeStr = '20150314'
startTime = datetime.strptime(str(startTimeStr), '%Y%m%d')
endTime = datetime.strptime(str(endTimeStr), '%Y%m%d')
delta = (endTime - startTime).days

playRecord = dict()

for day in range(0, delta):
    currentDate = datetime.strftime((startTime + timedelta(day)), "%Y%m%d")
    record = pd.read_csv(filepath_or_buffer="/home/frankfzw/Ali/demo/{}.csv".format(currentDate))
    playRecord[currentDate] = record

songList = playRecord.get(currentDate)['song_id'].values

print songList
