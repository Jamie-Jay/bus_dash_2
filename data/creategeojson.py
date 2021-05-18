import pandas as pd
import geojson
from geopy.distance import geodesic
import datetime

from datafeed import create_bus_speed_df as create_bus_speed_df

def compose_bus_stop_json(df_join):
    ## read stops file and get longtitude and latitude
    df_stop=pd.read_csv("stops.txt")
    stop_ids=df_stop['stop_id']
    stop_names=df_stop['stop_name']
    stop_lats=df_stop['stop_lat']
    stop_lons=df_stop['stop_lon']


    # stops with coordinates only
    # geo_json =  { \
    #   "type": "FeatureCollection", \
    #   "features": [ \
    #       {"type": "Feature", \
    #               "geometry": { \
    #                   "type": "LineString", \
    #                   "coordinates": [[lon, lat] \
    #               for lat, lon in zip(stop_lats,stop_lons) ] }}]}
    # geo_json_dic=geojson.dumps(geo_json)
    # f = open('geojson.json','w')
    # print (geo_json_dic, file=f)
    # f.close()


    # takes too long to render
    # geo_json =  { \
    #   "type": "FeatureCollection", \
    #   "features": [{ \
    #     "type": "Feature", \
    #     "geometry": { \
    #         "type": "Point", \
    #         "coordinates": [lon, lat] \
    #     }, \
    #     "properties": { \
    #       "name": str(id)+' '+str(name) \
    #     } \
    #   }
    #   for lat, lon, id, name in zip(stop_lats,stop_lons, stop_ids, stop_names)
    #   ]}

    geo_json =  { \
      "type": "FeatureCollection", \
      "features": [{ \
        "type": "Feature", \
        "geometry": { \
            "type": "MultiPoint", \
            "coordinates": [[lon, lat] \
              for lat, lon, id, name in zip(stop_lats,stop_lons, stop_ids, stop_names)] \
        }, \
        "properties": { \
          "names": [str(id)+' '+str(name) \
            for lat, lon, id, name in zip(stop_lats,stop_lons, stop_ids, stop_names)] \
        } \
      }
      ]
      }

    print(geo_json)
    geo_json_dic=geojson.dumps(geo_json)
    f = open('geojson.json','w')
    print (geo_json_dic, file=f)
    f.close()

############################ speed calc

def compose_bus_speed_json(df_join):
    pos_lats=df_join['lat']
    pos_lons=df_join['lon']
    pos_timestamps=df_join['timestamp']
    pos_route_shorts=df_join['route_short']
    pos_vehicle_ids=df_join['vehicle_id']
    pos_bearings=df_join['bearing']
    pos_destination_names=df_join['destination_name']
    pos_mphs=df_join['mph']

    geo_json =  { \
      "type": "FeatureCollection", \
      "features": [{ \
        "type": "Feature", \
        "geometry": { \
            "type": "MultiPoint", \
            "coordinates": [[lon, lat] \
              for lat, lon in zip(pos_lats,pos_lons)] \
        }, \
        "properties": { \
          "timestamp":[timestamp for timestamp in pos_timestamps], \
          "route_short":[route_short for route_short in pos_route_shorts], \
          "vehicle_id":[vehicle_id for vehicle_id in pos_vehicle_ids], \
          "bearing":[bearing for bearing in pos_bearings], \
          "destination_name":[destination_name for destination_name in pos_destination_names], \
          "mph":[mph for mph in pos_mphs], \
        } \
      }
      ]
      }

    geo_json_dic=geojson.dumps(geo_json)
    f = open('geospeedjson.json','w')
    print (geo_json_dic, file=f)
    f.close()

compose_bus_speed_json(create_bus_speed_df())