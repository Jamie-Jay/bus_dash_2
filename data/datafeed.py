# This file gives data feed

import pandas as pd
import numpy as np

# Initialize data frame
datafile='data/feb2021e149th.csv'
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