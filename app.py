import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import os

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Plotly mapbox public token
# "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_access_token = os.getenv('MAPBOX_API_KEY')


# Dictionary of important locations in New York
list_of_locations = {
    "Madison Square Garden": {"lat": 40.7505, "lon": -73.9934},
    "Yankee Stadium": {"lat": 40.8296, "lon": -73.9262},
    "Empire State Building": {"lat": 40.7484, "lon": -73.9857},
    "New York Stock Exchange": {"lat": 40.7069, "lon": -74.0113},
    "JFK Airport": {"lat": 40.644987, "lon": -73.785607},
    "Grand Central Station": {"lat": 40.7527, "lon": -73.9772},
    "Times Square": {"lat": 40.7589, "lon": -73.9851},
    "Columbia University": {"lat": 40.8075, "lon": -73.9626},
    "United Nations HQ": {"lat": 40.7489, "lon": -73.9680},
}

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

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("cornell-logo.png")
                        ),
                        html.H2("NYCBUSWATCHER VIEWER"),
                        html.P(
                            """This visualization shows observed bus positions on 4 routes  
                            serving the East 149th Street corridor in the Bronx.
                            Select different days using the 
                            date picker or by 
                            selecting
                            different time frames on the histogram."""
                        ),

                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2021, 2, 1),
                                    max_date_allowed=dt(2021, 2, 28),
                                    initial_visible_month=dt(2021, 2, 1),
                                    date=dt(2021, 2, 14).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),

                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[

                        # convert this to route selector
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for route on map
                                        dcc.Dropdown(
                                            id="route-selector",
                                            options=[
                                                {
                                                    "label": route, 
                                                    "value": route
                                                }
                                                for route in totalList.keys()
                                            ],
                                            placeholder="Select a route",
                                            value=list(totalList.keys())[0],
                                            multi=True
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="hour-selector",
                                            options=[
                                                {
                                                    "label": str(n) + ":00",
                                                    "value": str(n),
                                                }
                                                for n in range(24)
                                            ],
                                            multi=True,
                                            placeholder="Select certain hours",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-positions"),
                        html.P(id="total-positions-selection"),
                        html.P(id="date-value"),
                        dcc.Markdown(
                            children=[
                                "Source: [Cornell Tech Urban Tech Hub]("
                                "https://github.com/Cornell-Tech-Urban-Tech-Hub)"
                            ]
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            children=[
                                "Select any of the bars on the histogram to section data by time."
                            ],
                        ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)

# Gets the amount of days in the specified month
# Index represents month (0 is April, 1 is May, ... etc.)
daysInMonth = [28]

# Get index for the specified month in the dataframe
monthIndex = pd.Index(["Feb"])

# Select all routes when no routes are selected
def update_routes(routeSelected):
    if (routeSelected == None or len(routeSelected) == 0):
        routeSelected = list(totalList.keys())
    if isinstance(routeSelected, str):
        routeSelected = [routeSelected]

    return routeSelected

# Get the amount of rides per hour based on the time selected
# This also higlights the color of the histogram bars based on
# if the hours are selected
def get_selection(route, month, day, selection):
    xVal = []
    yVal = []
    xSelected = []
    colorVal = [
        "#F4EC15",
        "#DAF017",
        "#BBEC19",
        "#9DE81B",
        "#80E41D",
        "#66E01F",
        "#4CDC20",
        "#34D822",
        "#24D249",
        "#25D042",
        "#26CC58",
        "#28C86D",
        "#29C481",
        "#2AC093",
        "#2BBCA4",
        "#2BB5B8",
        "#2C99B4",
        "#2D7EB0",
        "#2D65AC",
        "#2E4EA4",
        "#2E38A4",
        "#3B2FA0",
        "#4E2F9C",
        "#603099",
    ]

    # Put selected times into a list of numbers xSelected
    xSelected.extend([int(x) for x in selection])

    for i in range(24):
        # If bar is selected then color it white
        if i in xSelected and len(xSelected) < 24:
            colorVal[i] = "#FFFFFF"
        xVal.append(i)
        # Get the number of rides at a particular time
        yVal.append(len(totalList[route][month][day][totalList[route][month][day].index.hour == i]))
    return [np.array(xVal), np.array(yVal), np.array(colorVal)]


# Selected Data in the Histogram updates the Values in the Hours selection dropdown menu
@app.callback(
    Output("hour-selector", "value"),
    [Input("histogram", "selectedData"), Input("histogram", "clickData")],
)
def update_hour_selector(value, clickData):
    holder = []
    if clickData:
        holder.append(str(int(clickData["points"][0]["x"])))
    if value:
        for x in value["points"]:
            holder.append(str(int(x["x"])))
    return list(set(holder))


# Clear Selected Data if Click Data is used
@app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
def update_selected_data(clickData):
    if clickData:
        return {"points": []}


# Update the total number of positions Tag
@app.callback(Output("total-positions", "children"), [Input("date-picker", "date")])
def update_total_positions(datePicked):
    date_picked = dt.strptime(datePicked, "%Y-%m-%d")

    total_pos = 0
    for value in totalList.values():
        total_pos += len(value[date_picked.month - 4][date_picked.day - 1])
    return "Total Number of bus positions: {:,d}".format(
        total_pos
    )


# Update the total number of positions in selected times
@app.callback(
    [Output("total-positions-selection", "children"), Output("date-value", "children")],
    [Input("route-selector", "value"), Input("date-picker", "date"), Input("hour-selector", "value")],
)
def update_total_positions_selection(routeSelected, datePicked, selection):
    firstOutput = ""

    if selection != None or len(selection) != 0:
        date_picked = dt.strptime(datePicked, "%Y-%m-%d")
        totalInSelection = 0
        
        routeSelected = update_routes(routeSelected)
        for r in routeSelected:
            for x in selection:
                totalInSelection += len(
                    totalList[r][date_picked.month - 4][date_picked.day - 1][
                        totalList[r][date_picked.month - 4][date_picked.day - 1].index.hour
                        == int(x)
                    ]
                )
        firstOutput = "Total positions in selection: {:,d}".format(totalInSelection)

    if (
        datePicked == None
        or selection == None
        or len(selection) == 24
        or len(selection) == 0
        or routeSelected == None
        or len(routeSelected) == 0
    ):
        return firstOutput, (datePicked, " - showing hour(s): All")

    holder = sorted([int(x) for x in selection])

    if holder == list(range(min(holder), max(holder) + 1)):
        return (
            firstOutput,
            (
                datePicked,
                " - showing hour(s): ",
                holder[0],
                "-",
                holder[len(holder) - 1],
            ),
        )

    holder_to_string = ", ".join(str(x) for x in holder)
    return firstOutput, (datePicked, " - showing hour(s): ", holder_to_string)


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
                marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
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


# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("route-selector", "value"),
        Input("date-picker", "date"),
        Input("hour-selector", "value"),
        # Input("location-dropdown", "value"),
    ],
)
#def update_graph(datePicked, selectedData, selectedLocation):
def update_graph(routeSelected, datePicked, selectedData):
    zoom = 12.0
    latInitial = 40.8167
    lonInitial = -73.9199
    bearing = 0

    # if selectedLocation:
    #     zoom = 15.0
    #     latInitial = list_of_locations[selectedLocation]["lat"]
    #     lonInitial = list_of_locations[selectedLocation]["lon"]

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
                    color=np.append(np.insert(listCoords.index.hour, 0, 0), 23),
                    opacity=0.5,
                    size=5,
                    colorscale=[
                        [0, "#F4EC15"],
                        [0.04167, "#DAF017"],
                        [0.0833, "#BBEC19"],
                        [0.125, "#9DE81B"],
                        [0.1667, "#80E41D"],
                        [0.2083, "#66E01F"],
                        [0.25, "#4CDC20"],
                        [0.292, "#34D822"],
                        [0.333, "#24D249"],
                        [0.375, "#25D042"],
                        [0.4167, "#26CC58"],
                        [0.4583, "#28C86D"],
                        [0.50, "#29C481"],
                        [0.54167, "#2AC093"],
                        [0.5833, "#2BBCA4"],
                        [1.0, "#613099"],
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

    # return go.Figure(
    #     data=[
            # # Plot of important locations on the map
            # Scattermapbox(
            #     lat=[list_of_locations[i]["lat"] for i in list_of_locations],
            #     lon=[list_of_locations[i]["lon"] for i in list_of_locations],
            #     mode="markers",
            #     hoverinfo="text",
            #     text=[i for i in list_of_locations],
            #     marker=dict(size=8, color="#ffa0a0"),
            # ),
        # ],
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
            accesstoken=mapbox_access_token,
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


if __name__ == "__main__":
    app.run_server(debug=True)
