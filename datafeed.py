# This file gives data feed

import pandas as pd
import numpy as np

# Initialize data frame
datafile='feb2021e149th.csv'
df=pd.read_csv(datafile, sep='\t', skiprows=1)

# Get a dict containing lists of position counts per bus route, month, day
totalList = {}
for df_route in df.groupby('route_short'):

    df_route[1]["Date/Time"] = pd.to_datetime(df_route[1]["timestamp"], format="%Y-%m-%d %H:%M:%S") # verify/update format
    df_route[1].index = df_route[1]["Date/Time"]
    df_route[1].drop("Date/Time", 1, inplace=True)

    routeList = []
    for month in df_route[1].groupby(df_route[1].index.month):
        dailyList = []
        for day in month[1].groupby(month[1].index.day):
            dailyList.append(day[1])
        routeList.append(dailyList)
    routeList = np.array(routeList,dtype=object)
    
    totalList[df_route[0]] = routeList
