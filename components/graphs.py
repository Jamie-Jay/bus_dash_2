from dash.dependencies import Input, Output

from plotly import graph_objs as go
from plotly.graph_objs import *
import plotly.express as px

from datetime import datetime as dt
import numpy as np
import pandas as pd
import json

import sys
sys.path.append('../')
import data.datafeed as df
from data.datafeed import totalList as totalList
from data.datafeed import get_selected_data as get_selected_data
from data.datafeed import add_distance as add_distance
from data.datafeed import get_selected_time as get_selected_time
import data.constants as constants

from app import app

# Select all routes when no routes are selected
def update_routes(routeSelected):
    if (routeSelected == None or len(routeSelected) == 0):
        routeSelected = list(totalList.keys())
    if isinstance(routeSelected, str):
        routeSelected = [routeSelected]

    return routeSelected

# Get the Coordinates of the chosen months, dates and times
def getLatLonColor(route, selectedData, month, day):
    listCoords = totalList[route][month][day]

    # No times selected, output all times for chosen month and date
    if selectedData == None or len(selectedData) == 0:
        return listCoords
    listStr = "listCoords["
    for time in selectedData:
        if selectedData.index(time) != len(selectedData) - 1:
            listStr += "(totalList[route][month][day].index.hour==" + str(int(time)) + ") | "
        else:
            listStr += "(totalList[route][month][day].index.hour==" + str(int(time)) + ")]"
    return eval(listStr)

# Static map for now - show bus positions
# @app.callback(
#     Output("map-graph-static", "figure"),
    # [
    #     Input("route-selector", "value"),
    #     Input("date-picker", "date"),
    #     Input("hour-selector", "value"),
    # ],
# )
def update_graph_static():    
    with open('data/geojson.json') as json_file:
        geo_json = json.load(json_file)

    latInitial = 40.8167
    lonInitial = -73.9199

    fig = go.Figure(
        data=[
            go.Scattermapbox(
                lat=np.array(feature["geometry"]["coordinates"])[:, 1], # MultiPoint
                lon=np.array(feature["geometry"]["coordinates"])[:, 0],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=9
                ),
                text=np.array(feature["properties"]["names"]),
            )
            for feature in geo_json["features"]
        ]
    )
  
    fig.update_layout(
        autosize=True,
        margin=go.layout.Margin(l=0, r=0, t=0, b=0),
        hovermode='closest',
        mapbox=dict(
            style="stamen-terrain", 
            accesstoken=constants.mapbox_access_token,
            bearing=0,
            center=dict(lat=latInitial, lon=lonInitial),
            pitch=0,
            zoom=12,
        ),
        height=600
    )

    return fig

# Show travel speed for now
@app.callback(
    Output("map-graph-animated", "figure"),
    [
        Input("route-selector", "value"),
        Input("route-d-selector", "value"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("hour-range-selector", "value"),
    ],
)
def update_graph_animated(routeSelected, direction, startDate, endDate, selectedHour):
    df_animated = get_selected_data(routeSelected, direction, startDate, endDate, selectedHour)
    # print(df_animated.shape) # TODO: add the count info to webpage
    df_animated['mph']= df_animated['mph'].fillna(0)
    # user care more about slow speed, use 1/mph to show speed
    df_animated["1/mph"] = 1 / df_animated["mph"]
    df_animated['1/mph'][np.isinf(df_animated['1/mph'])] = 0

    fig = px.scatter_mapbox(df_animated, lon="lon", lat="lat", animation_frame="timestamp",
           size="1/mph", color="route_short", hover_name="destination_name", size_max=55
                        )

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=go.layout.Mapbox(
            style="stamen-terrain", 
            zoom=12, 
            center_lat = 40.8167,
            center_lon = -73.9199,
        ),
        # width=800,
        height=600,
    )

    return fig

# Show travel speed histo
@app.callback(
    [
        Output("time-options", "options"), 
        Output("time-options", "value")
    ],
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("hour-range-selector", "value"),
    ],
)
def update_time_radioitems(startDate, endDate, selectedHour):
    hours = get_selected_time(startDate, endDate, selectedHour)
    
    timeOptions = []
    for h in hours:
        timeOptions.append(h.strftime("%Y-%m-%d %H:00"))

    options=[{'label': x, 'value': x} 
              for x in timeOptions]
    return options, timeOptions[0]

def get_time_option_data(routeSelected, direction, timeOption):
    target = dt.strptime(timeOption, '%Y-%m-%d %H:00')
    start_Date = target.strftime("%Y-%m-%d")
    end_Date = None
    time_option = [target.hour, target.hour+1]

    df_timeOption = get_selected_data(routeSelected, direction, start_Date, end_Date, time_option)

    return df_timeOption

def update_heatmap_layout(fig):
    fig.update_layout(
        xaxis = dict(
            #color='#444',
            title=dict(
                text='Timestamp',# 标题的文字
                font = dict(
                    #  family = '',  # 字体 比如宋体
                        size = 12,    # 标题大小   
                    #  color = '',   # 在此处可以只设置标题的颜色
                        ),
                standoff = 1, # 设置标题和标签的距离，大于等于0的数字，注意标题是不会超出页边的   
            ),
            # showgrid=False,
        ),
        yaxis = dict(
            #color='#444',
            title=dict(
                text='Distance(Miles)',# 标题的文字
                font = dict(
                    #  family = '',  # 字体 比如宋体
                        size = 12,    # 标题大小   
                    #  color = '',   # 在此处可以只设置标题的颜色
                        ),
                standoff = 1, # 设置标题和标签的距离，大于等于0的数字，注意标题是不会超出页边的   
            ),
            # showgrid=False,
        ),
        # showlegend=False,
        plot_bgcolor="#323130",
        paper_bgcolor="#323130",
        dragmode="select",
        font=dict(color="white"),
        margin=go.layout.Margin(l=50, r=50, t=50, b=50),
    )
    # layout = go.Layout(
    #         bargap=0.01,
    #         bargroupgap=0,
    #         barmode="group",
    #         margin=go.layout.Margin(l=10, r=0, t=0, b=50),
    #         showlegend=False,
    #         plot_bgcolor="#323130",
    #         paper_bgcolor="#323130",
    #         dragmode="select",
    #         font=dict(color="white"),
    #         xaxis=dict(
    #             # range=[-0.5, 23.5],
    #             showgrid=False,
    #             nticks=25,
    #             fixedrange=True,
    #             ticksuffix=":00",
    #         ),
    #         yaxis=dict(
    #             # range=[0, max(yVals) + max(yVals) / 4],
    #             showticklabels=False,
    #             showgrid=False,
    #             fixedrange=True,
    #             rangemode="nonnegative",
    #             zeroline=False,
    #         ),
    #         annotations=[
    #             dict(
    #                 x=xi,
    #                 y=yi,
    #                 text=str(yi),
    #                 xanchor="center",
    #                 yanchor="bottom",
    #                 showarrow=False,
    #                 font=dict(color="white"),
    #             )
    #             for xi, yi in zip(xVals, yVals)
    #         ],
    #     )

# Show travel speed heatmap
@app.callback(
    Output("speedHeatMap", "figure"),
    [
        Input("route-selector", "value"),
        Input("route-d-selector", "value"),
        Input("time-options", "value"),
    ],
)
def update_travel_speed(routeSelected, direction, timeOption):

    df_timeOption = get_time_option_data(routeSelected, direction, timeOption)
    df_timeOption = add_distance(df_timeOption)

    fig = go.Figure(
        data=go.Heatmap(
            z=df_timeOption['mph'],
            x=df_timeOption['timestamp'],
            y=df_timeOption['distance'],
            colorscale='Viridis' # https://plotly.com/python/builtin-colorscales/
        )
    )

    # title='HeatMap - Travel Speed (mph)',
    update_heatmap_layout(fig)

    return fig


# Show bunching heatmap
@app.callback(
    Output("bunchingHeatMap", "figure"),
    [
        Input("route-selector", "value"),
        Input("route-d-selector", "value"),
        Input("time-options", "value"),
    ],
)
def update_bunching(routeSelected, direction, timeOption):

    df_timeOption = get_time_option_data(routeSelected, direction, timeOption)
    # df_timeOption = df_timeOption[df_timeOption['bunch_count']!=0] # do not show 0 bunching, or show 0 as grey color
    df_timeOption = add_distance(df_timeOption)

    fig = go.Figure(
        data=go.Heatmap(
            z=df_timeOption['bunch_count'],
            x=df_timeOption['timestamp'],
            y=df_timeOption['distance'],
            colorscale='Viridis'
        )
    )

    # title='HeatMap - Bunching Count',
    update_heatmap_layout(fig)

    return fig

# Show if dwelling heatmap
@app.callback(
    Output("dwellingHeatMap", "figure"),
    [
        Input("route-selector", "value"),
        Input("route-d-selector", "value"),
        Input("time-options", "value"),
    ],
)
def update_dwell_time(routeSelected, direction, timeOption):
    
    df_timeOption = get_time_option_data(routeSelected, direction, timeOption)
    df_timeOption = add_distance(df_timeOption)
    df_timeOption['dwelling'] = df_timeOption['dwelling'].astype('int') # change False to 0, True to 1

    fig = go.Figure(
        data=go.Heatmap(
            z=df_timeOption['dwelling'],
            x=df_timeOption['timestamp'],
            y=df_timeOption['distance'],
            colorscale='Viridis'
        )
    )

    # title='HeatMap - If Dwelling (1 represents it is dwelling)', 
    update_heatmap_layout(fig)

    return fig

# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("route-selector", "value"),
        Input("date-picker", "date"),
        Input("hour-selector", "value"),
    ],
)
def update_graph(routeSelected, datePicked, selectedData):
    zoom = 12.0
    latInitial = 40.8167
    lonInitial = -73.9199
    bearing = 0

    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    monthPicked = date_picked.month - 4
    dayPicked = date_picked.day - 1

    res = []
    xVals = []
    yVals = []
    routeSelected = update_routes(routeSelected)
    for r in routeSelected:
        listCoords = getLatLonColor(r, selectedData, monthPicked, dayPicked)

        res.append(
            # Data for all rides based on date and time
            Scattermapbox(
                lat=listCoords["lat"],
                lon=listCoords["lon"],
                name=r,
                mode="markers",
                hoverinfo="lat+lon+text",
                text=listCoords.index.hour,
                marker=dict(
                    showscale=True,
                    color=np.append(
                        np.insert(listCoords.index.hour, 0, 0),
                        23),
                    opacity=0.5,
                    size=5,
                    colorscale=[
                        [i / (len(constants.colorVal) - 1), v] for i, v in enumerate(constants.colorVal)
                    ],
                    colorbar=dict(
                        title="Time of<br>Day",
                        x=0.93,
                        xpad=0,
                        nticks=24,
                        tickfont=dict(color="#d8d8d8"),
                        titlefont=dict(color="#d8d8d8"),
                        thicknessmode="pixels",
                    ),
                ),
            )
        )

    layout=Layout(
        autosize=True,
        margin=go.layout.Margin(l=0, r=35, t=0, b=0),
        showlegend=True,
        legend=dict(
            x=0.05,
            y=0.1,
            bgcolor='rgba(255,255,255 ,0.1)',
            font=dict(
                size=12,
                color='white'
            )
        ),
        legend_title='<b> Route </b>',
        legend_title_font_color='white',
        mapbox=dict(
            accesstoken=constants.mapbox_access_token,
            center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
            style="dark",
            bearing=bearing,
            zoom=zoom,
        ),
        updatemenus=[
            dict(
                buttons=(
                    [
                        dict(
                            args=[
                                {
                                    "mapbox.zoom": 12,
                                    "mapbox.center.lon": "-73.991251",
                                    "mapbox.center.lat": "40.7272",
                                    "mapbox.bearing": 0,
                                    "mapbox.style": "dark",
                                }
                            ],
                            label="Reset Zoom",
                            method="relayout",
                        )
                    ]
                ),
                direction="left",
                pad={"r": 0, "t": 0, "b": 0, "l": 0},
                showactive=False,
                type="buttons",
                x=0.45,
                y=0.02,
                xanchor="left",
                yanchor="bottom",
                bgcolor="#323130",
                borderwidth=1,
                bordercolor="#6d6d6d",
                font=dict(color="#FFFFFF"),
            )
        ],
    )

    return go.Figure(
        data=res,
        layout=layout
        )


# Get the amount of rides per hour based on the time selected
# This also higlights the color of the histogram bars based on
# if the hours are selected
def get_selection(route, month, day, selection):
    xVal = []
    yVal = []
    xSelected = []
    colorVal = constants.colorVal[:]

    # Put selected times into a list of numbers xSelected
    xSelected.extend([int(x) for x in selection])

    for i in range(24):
        # If bar is selected then color it white
        if i in xSelected and len(xSelected) < 24:
            colorVal[i] = "#FFFFFF"
        xVal.append(i)
        # Get the number of rides at a particular time
        yVal.append(len(totalList[route][month][day]
                    [totalList[route][month][day].index.hour == i]))
    return [np.array(xVal), np.array(yVal), np.array(colorVal)]


# Update Histogram Figure based on Month, Day and Times Chosen
@app.callback(
    Output("histogram", "figure"),
    [Input("route-selector", "value"), Input("date-picker", "date"), Input("hour-selector", "value")],
)
def update_histogram(routeSelected, datePicked, selection):
    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    monthPicked = date_picked.month - 4
    dayPicked = date_picked.day - 1

    res = []
    xVals = []
    yVals = []
    routeSelected = update_routes(routeSelected)
    for r in routeSelected:
        [xVal, yVal, colorVal] = get_selection(r, monthPicked, dayPicked, selection)
        xVals.extend(xVal)
        yVals.extend(yVal)

        res.append(
            go.Bar(
                x=xVal,
                y=yVal,
                name=r,
                marker=dict(color=colorVal), hoverinfo="x"
            )
        )

        res.append(
            go.Scatter(
                opacity=0,
                x=xVal,
                y=yVal,
                name=r,
                # hoverinfo="none",
                mode="markers+lines",
                marker=dict(
                    color="rgb(66, 134, 244, 0)",
                    symbol="square", 
                    size=40
                ),
                visible=True,
            )
        )

    layout = go.Layout(
            bargap=0.01,
            bargroupgap=0,
            barmode="group",
            margin=go.layout.Margin(l=10, r=0, t=0, b=50),
            showlegend=False,
            plot_bgcolor="#323130",
            paper_bgcolor="#323130",
            dragmode="select",
            font=dict(color="white"),
            xaxis=dict(
                range=[-0.5, 23.5],
                showgrid=False,
                nticks=25,
                fixedrange=True,
                ticksuffix=":00",
            ),
            yaxis=dict(
                range=[0, max(yVals) + max(yVals) / 4],
                showticklabels=False,
                showgrid=False,
                fixedrange=True,
                rangemode="nonnegative",
                zeroline=False,
            ),
            annotations=[
                dict(
                    x=xi,
                    y=yi,
                    text=str(yi),
                    xanchor="center",
                    yanchor="bottom",
                    showarrow=False,
                    font=dict(color="white"),
                )
                for xi, yi in zip(xVals, yVals)
            ],
        )

    return go.Figure(
        data=res,
        layout=layout,
    )