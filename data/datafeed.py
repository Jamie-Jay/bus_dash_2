# This file gives data feed

import pandas as pd
import numpy as np
import datetime
from geopy.distance import geodesic

# Initialize data frame
# datafile='data/feb2021e149th.csv'
datafile='data/feb2021e149th_Bx19_processed.csv'
# df=pd.read_csv(datafile, sep='\t', skiprows=1)
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

def get_selected_data(routeSelected, direction, startDate, endDate, selectedHour):
    df_output = df

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
    if(startDate!= None and endDate != None and selectedHour != None): # TODO: support multiple datePicked
        # get target time range
        d_s = datetime.datetime.strptime(startDate[:len('2021-02-15')], '%Y-%m-%d')
        d_e = datetime.datetime.strptime(endDate[:len('2021-02-15')], '%Y-%m-%d')

        df_output['timestamp'] = df_output['timestamp'].astype('datetime64[ns]') # <class 'pandas._libs.tslibs.timestamps.Timestamp'> Pandas replacement for datetime.datetime

        d = d_s
        delta = datetime.timedelta(days=1)
        join_cols = df_output.columns.values.tolist()
        df_join = pd.DataFrame(columns=join_cols)
        while d <= d_e:
            # print (d.strftime("%Y-%m-%d"))
            start_time = datetime.datetime(d.year, d.month, d.day, selectedHour[0])
            end_time = datetime.datetime(d.year, d.month, d.day, selectedHour[1])
            print(start_time, end_time)
            df_output_d = df_output[df_output['timestamp']>=pd.Timestamp(start_time)]
            df_output_d = df_output_d[df_output_d['timestamp']<pd.Timestamp(end_time)]

            df_join = pd.concat([df_join,df_output_d],axis=0)
            d += delta

        df_output=df_join
        df_output['timestamp'] = df_output['timestamp'].astype('str')

    return (df_output)

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

# df_output = create_bus_speed_df(df)
# df_output.to_csv('newdf.csv')



# # travel speed

# # group by trip id+service day+vehicle id
# # service_date/trip_id/vehicle_id
# for df_route in df.groupby(['route_short', 'service_date', 'trip_id', 'vehicle_id']):



# df_bx19 = df.loc[df['route_short'] == 'Bx19', :]

# # references
# # https://en.wikipedia.org/wiki/World_Geodetic_System
# # https://gis.stackexchange.com/questions/48949/epsg-3857-or-4326-for-googlemaps-openstreetmap-and-leaflet
# # https://en.wikipedia.org/wiki/EPSG_Geodetic_Parameter_Dataset

# # https://spatialreference.org/ref/epsg/4326/
# crs_wgs84 = 4326  # WGS84, Latitute/Longitude, used by GPS

# # https://spatialreference.org/ref/epsg/2263/
# crs_epsg2263 = 2263  # NAD83 / New York Long Island (ftUS)
# gdf_bx19 = gpd.GeoDataFrame(df_bx19, crs=crs_wgs84, geometry=gpd.points_from_xy(df_bx19['lon'], df_bx19['lat'])).to_crs(crs=crs_epsg2263)

# gdf_bx19_NYCT_721 = gdf_bx19.loc[gdf_bx19['vehicle_id'] == 'MTA NYCT_721', :]

# min_timestamp = gdf_bx19_NYCT_721['timestamp'].min()

# gdf_bx19_NYCT_721.reset_index(drop=True, inplace=True)

# # function to calculate mph
# def calc_mph(coord1, coord2, time1, time2):
#     if pd.isnull(time2):
#         return
#     else:
#         dist = float(geodesic(coord1, coord2).miles)
#         hrs = float(pd.Timedelta(time2-time1).total_seconds()) / (60.0 * 60.0)  # divide by 60 * 60 for hours
#         return dist / hrs

# gdf_bx19_NYCT_721_shifted = gdf_bx19_NYCT_721.shift(periods=-1)

# # merge timestamp, lat, and lon columns from shifted df to non-shifted df
# gdf_bx19_NYCT_721_mph = gdf_bx19_NYCT_721.merge(gdf_bx19_NYCT_721_shifted[['timestamp', 'lat', 'lon']],
#                                                 how='inner', left_index=True, right_index=True,
#                                                 suffixes=('', '_next'))

# gdf_bx19_NYCT_721_mph['mph'] = gdf_bx19_NYCT_721_mph.apply(lambda x:
#                                                            calc_mph(coord1=(x['lat'], x['lon']),
#                                                                     coord2=(x['lat_next'], x['lon_next']),
#                                                                     time1=x['timestamp'],
#                                                                     time2=x['timestamp_next']), axis=1)