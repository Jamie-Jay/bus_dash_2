import pandas as pd
import geojson

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