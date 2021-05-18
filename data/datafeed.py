# This file gives data feed

import pandas as pd
import numpy as np
import datetime
from geopy.distance import geodesic

# Initialize data frame
# datafile='data/feb2021e149th.csv'
# df=pd.read_csv(datafile, sep='\t', skiprows=1)
datafile='data/feb2021e149th_Bx19_processed.csv'
df=pd.read_csv(datafile)
# new cols: dwelling, bunch_flag, mph

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

def get_selected_time(startDate, endDate, selectedHour):
    times = []

    if(startDate!= None and selectedHour != None):
        d_s = datetime.datetime.strptime(startDate[:len('2021-02-15')], '%Y-%m-%d')
        # print(d_s)

        if (endDate != None): # date range
            d_e = datetime.datetime.strptime(endDate[:len('2021-02-15')], '%Y-%m-%d')
            d = d_s
            delta = datetime.timedelta(days=1)
            while d <= d_e:
                # print (d.strftime("%Y-%m-%d"))
                for t in range(selectedHour[0], selectedHour[1]):
                    times.append(datetime.datetime(d.year, d.month, d.day, t))
                d += delta

        else: # single range
            for t in range(selectedHour[0], selectedHour[1]):
                times.append(datetime.datetime(d_s.year, d_s.month, d_s.day, t))

    return times

# support both single date and date range
# single date: endDate is None
def get_selected_data(routeSelected, direction, startDate, endDate, selectedHour):
    df_output = df.copy(deep=True)

    # print(routeSelected)
    if(routeSelected != None):
        if(isinstance(routeSelected, list) == False): # compatible with radioItem and checklist
            routeSelected = [routeSelected]
        for route in routeSelected:
            df_output = df_output[df_output['route_short']==route]
    
    # print(direction)
    if(direction != None):
        for dr in direction:
            df_output = df_output[df_output['direction']==dr]

    # print(startDate, endDate)
    # print(selectedHour)
    if(startDate!= None and selectedHour != None):
        d_s = datetime.datetime.strptime(startDate[:len('2021-02-15')], '%Y-%m-%d')
        df_output['timestamp'] = df_output['timestamp'].astype('datetime64[ns]') # <class 'pandas._libs.tslibs.timestamps.Timestamp'> Pandas replacement for datetime.datetime

        if (endDate != None): # date range
            # get target time range
            d_e = datetime.datetime.strptime(endDate[:len('2021-02-15')], '%Y-%m-%d')

            d = d_s
            delta = datetime.timedelta(days=1)
            join_cols = df_output.columns.values.tolist()
            df_join = pd.DataFrame(columns=join_cols)
            while d <= d_e:
                # print (d.strftime("%Y-%m-%d"))
                start_time = datetime.datetime(d.year, d.month, d.day, selectedHour[0])
                end_time = datetime.datetime(d.year, d.month, d.day, selectedHour[1])
                # print(start_time, end_time)
                df_output_d = df_output[df_output['timestamp']>=pd.Timestamp(start_time)]
                df_output_d = df_output_d[df_output_d['timestamp']<pd.Timestamp(end_time)]

                df_join = pd.concat([df_join,df_output_d],axis=0)
                d += delta

            df_output = df_join
        else: # single range
            start_time = datetime.datetime(d_s.year, d_s.month, d_s.day, selectedHour[0])
            end_time = datetime.datetime(d_s.year, d_s.month, d_s.day, selectedHour[1])
            df_output = df_output[df_output['timestamp']>=pd.Timestamp(start_time)][df_output['timestamp']<pd.Timestamp(end_time)]

        df_output['timestamp'] = df_output['timestamp'].astype('str')

    # print(df_output.shape)

    return (df_output)

def calc_distance(coord1, coord2):
    dist = float(geodesic(coord1, coord2).miles)
    return round(dist, 1)

def add_distance(df_input):
    df_input_dist = df_input.copy(deep=True)

    # anchor point: first point of df_input
    # lat_s = df_input_dist.iloc[0]['lat'] 
    # lon_s = df_input_dist.iloc[0]['lon']
    # # print (lon_s, lat_s)
    # df_input_dist['distance'] = df_input_dist.apply(lambda x:
    #                                         calc_distance(coord1=(lat_s, lon_s),
    #                                                 coord2=(x['lat'], x['lon'])), axis=1)

    # anchor point: first point of every trip_id
    df_input_dist['distance'] = df_input_dist.apply(lambda x:
                                        calc_distance(coord1=(df_input_dist[df_input_dist['trip_id']==x['trip_id']].iloc[0]['lat'], 
                                                                df_input_dist[df_input_dist['trip_id']==x['trip_id']].iloc[0]['lon']),
                                                    coord2=(x['lat'], x['lon'])), axis=1)

    return df_input_dist

def calc_mph(coord1, coord2, time1, time2):
    if pd.isnull(time2):
        return
    else:
        dist = float(geodesic(coord1, coord2).miles)
        # hrs = float(pd.Timedelta(time2-time1).total_seconds()) / (60.0 * 60.0)  # divide by 60 * 60 for hours
        d1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
        hrs = (d2-d1).seconds / (60.0 * 60.0)
        
        if (hrs == 0):
            print (coord1, coord2, time1, time2)
        return dist / hrs

def calc_mph_df(df_input):
    df_input_shifted = df_input.shift(periods=1)

    # merge timestamp, lat, and lon columns from shifted df to non-shifted df
    df_input_mph = df_input.merge(df_input_shifted[['timestamp', 'lat', 'lon']],
                                                    how='inner', left_index=True, right_index=True,
                                                    suffixes=('', '_next'))


    df_input_mph['mph'] = df_input_mph.apply(lambda x:
                                            calc_mph(coord1=(x['lat'], x['lon']),
                                                    coord2=(x['lat_next'], x['lon_next']),
                                                    time1=x['timestamp'],
                                                    time2=x['timestamp_next']), axis=1)
    # fill in the first row's speed as the same as the second row
    if(df_input_mph.shape[0] > 1):
        df_input_mph.iloc[0,-1] = df_input_mph.iloc[1,-1]
    
    return df_input_mph

def create_bus_speed_df(df_input):
    df_input.sort_values(by="timestamp" , ascending=False)
    
    join_cols = df_input.columns.values.tolist()
    join_cols.append('mph')
    df_join = pd.DataFrame(columns=join_cols)

    for vh in set(df_input['vehicle_id'].values):
        vh_df = df_input[df_input['vehicle_id']==vh]
        vh_df_mph = calc_mph_df(vh_df)
        df_join = pd.concat([df_join,vh_df_mph],axis=0)

    return df_join