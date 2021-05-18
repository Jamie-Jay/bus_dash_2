import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from datetime import datetime as dt

import sys
sys.path.append('../')
from data.datafeed import totalList as totalList
import components.graphs

from app import app

route_selector = dbc.FormGroup(
    [
        dbc.Label("Route", className='h3'),
        dcc.Checklist(
            id="route-selector",
            options=[
                {
                    "label": route,
                    "value": route
                }
                for route in totalList.keys()
            ],
            labelStyle={'display': 'inline-block'}
        ),
    ]
)

route_direction = dbc.FormGroup(
    [
        dbc.Label("Route Direction", className='h3'),
        dcc.Checklist(
            id="route-d-selector",
            options=[ # TODO: update the direction options dynamically
                {"label": "0", "value": 0},
                {"label": "1", "value": 1}
            ],
            # inline=True,
        ),
    ]
)

date_range = dbc.FormGroup(
    [
        dbc.Label("Date Range", className='h3'),
        dcc.DatePickerRange(
            id="date-picker",
            min_date_allowed=dt(2021, 2, 1),
            max_date_allowed=dt(2021, 2, 28),
            initial_visible_month=dt(2021, 2, 1),
            start_date=dt(2021, 2, 3),
            end_date=dt(2021, 2, 4),
            display_format="MMMM D, YYYY",
            minimum_nights=0, # allow picking one day
            # calendar_orientation='vertical',
            style={"border": "0px solid black", 'background-color':'#000000'},
        )
    ]
)


time_range = dbc.FormGroup(
    [
        dbc.Label("Time of a day", html_for="range-slider", className='h3'),
        dcc.RangeSlider(
            id="hour-range-selector", 
            min=0, max=24, 
            value=[6, 8], 
            marks={i: str(i) for i in range(0, 25)}
        ),
        dbc.RadioItems(
            id="time-selector-special",
            options=[
                {"label": "morning rush(6-10am)", "value": 1},
                {"label": "evening rush(3-7pm)", "value": 2},
                {"label": "school dismissal time(3-4pm)", "value": 3},
                {"label": "night time(8pm-11pm)", "value": 4,},
                {"label": "owl period(0am-6am)", "value": 5,},
                {"label": "all day", "value": 6,},
            ],
            value=[],
            inline=True,
        ),
    ]
)

day_range = dbc.FormGroup(
    [
        dbc.Label("Day of a week", html_for="dropdown", className='h3'),
        dcc.Dropdown(
            id="day-selector",
            options=[
                {"value": 1, "label": "Monday"},
                {"value": 2, "label": "Tues"},
                {"value": 3, "label": "Wed"},
                {"value": 4, "label": "Thur"},
                {"value": 5, "label": "Fri"},
                {"value": 6, "label": "Sat"},
                {"value": 7, "label": "Sun"}
            ],
            multi=True,
            placeholder="Select certain days",
        ),
        dbc.RadioItems(
            id="day-selector-special",
            options=[
                {"label": "Weekday only", "value": 1},
                {"label": "Weekend only", "value": 2},
                {"label": "Saturday", "value": 3},
                {"label": "Sunday", "value": 4},
                {"label": "All week", "value": 5},
            ],
            value=[],
            inline=True,
        ),
    ]
)

# slider = dbc.FormGroup(
#     [
#         dbc.Label("Slider", html_for="slider"),
#         dcc.Slider(id="slider", min=0, max=10, step=0.5, value=3),
#     ]
# )

# range_slider = dbc.FormGroup(
#     [
#         dbc.Label("RangeSlider", html_for="range-slider", className='h3'),
#         dcc.RangeSlider(id="range-slider", min=0, max=23, value=[6, 8], 
#         marks={i: str(i) for i in range(0, 24)},
#                             ),
#     ]
# )

aggregate_opt = dbc.FormGroup(
    [
        dbc.Label("By hour aggregation"),
        # dbc.RadioItems(
        #     id="aggregate-opt",
        #     options=[
        #         {"label": "by hour", "value": 1},
        #         {"label": "by day", "value": 2},
        #         {"label": "by week", "value": 3},
        #         {"label": "by month", "value": 4},
        #     ],
        #     value=[2],
        # ),
        dcc.RadioItems(
            id='time-options',
            # options=[{'label': x, 'value': x} 
            #         for x in df.columns],
            # value=df.columns.tolist(),
        ),
    ]
)


tab1_content = dbc.Card(
    dbc.CardBody(
        [
            # html.P("This is tab 1!", className="card-text"),
            dbc.Form([route_selector, route_direction])
        ]
    ),
    className="mt-3",
    color='#323130'
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            # html.P("This is tab 2!", className="card-text"),
            # dbc.Form([time_range, day_range, date_range]) # TODO: add interactive day_range
            dbc.Form([time_range, date_range])
        ]
    ),
    className="mt-3",
    color='#323130'
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            # html.P("This is tab 2!", className="card-text"),
            aggregate_opt
        ]
    ),
    className="mt-3",
    color='#323130'
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Route filter"),
        dbc.Tab(tab2_content, label="Time filter"),
        dbc.Tab(
            # "This tab's content is never seen", 
            tab3_content, label="Aggregrate", disabled=False
        ),
    ]
)

# time tab relationship
@app.callback(
    Output("hour-range-selector", "value"),
    [
        Input("time-selector-special", "value"),
    ],
)
def time_special_change(radio_items_value):
    if radio_items_value == 1: # morning rush(6-10am)
        return [6, 10]
    elif radio_items_value == 2: # evening rush(3-7pm)
        return [15, 19]
    elif radio_items_value == 3: # school dismissal time(3-4pm)
        return [15, 16]
    elif radio_items_value == 4: # night time(8pm-11pm)
        return [20, 23]
    elif radio_items_value == 5: # owl period(0am-6am)
        return [0, 6]
    elif radio_items_value == 6: # all day
        return [0, 24]
    return [8, 10]

# day tab relationship
@app.callback(
    Output("day-selector", "value"),
    [
        Input("day-selector-special", "value"),
    ],
)
def time_special_change(radio_items_value):
    if radio_items_value == 1: # Weekday only
        return [1, 2, 3, 4, 5]
    elif radio_items_value == 2: # Weekend only
        return [6, 7]
    elif radio_items_value == 3: # Saturday
        return [6]
    elif radio_items_value == 4: # Sunday
        return [7]
    elif radio_items_value == 5: # All weekday
        return [1, 2, 3, 4, 5, 6, 7]
    return [1]