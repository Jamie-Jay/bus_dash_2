import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from datetime import datetime as dt

import sys
sys.path.append('../')
from data.datafeed import totalList as totalList

route_selector = dbc.FormGroup(
    [
        dbc.Label("Route", html_for="dropdown"),
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
        ),
    ]
)

route_direction = dbc.FormGroup(
    [
        dbc.Label("Route Direction", html_for="dropdown"),
        dcc.Checklist(
            id="route-d-selector",
            options=[
                {
                    "label": "0", "value": 0
                },
                {
                    "label": "1", "value": 1,
                }
            ],
            # inline=True,
        ),
    ]
)

date_range = dbc.FormGroup(
    [
        dbc.Label("Date"),
        dcc.DatePickerSingle(
            id="date-picker",
            min_date_allowed=dt(2021, 2, 1),
            max_date_allowed=dt(2021, 2, 28),
            initial_visible_month=dt(2021, 2, 1),
            date=dt(2021, 2, 14).date(),
            display_format="MMMM D, YYYY",
            style={"border": "0px solid black"},
        )
    ]
)


time_range = dbc.FormGroup(
    [
        dbc.Label("Time of a day", html_for="range-slider"),
        dcc.RangeSlider(
            id="hour-selector", 
            min=0, max=23, 
            value=[6, 8], 
            marks={i: str(i) for i in range(0, 24)}
        ),
        dbc.RadioItems(
            id="time-selector-special",
            options=[
                {"label": "morning rush", "value": 1},
                {"label": "evening rush", "value": 2},
                {"label": "school dismissal time", "value": 3},
                {"label": "night time", "value": 4,},
                {"label": "owl period", "value": 5,},
            ],
            value=[],
        ),
    ]
)

day_range = dbc.FormGroup(
    [
        dbc.Label("Day of a week", html_for="dropdown"),
        dcc.Dropdown(
            id="day-selector",
            options=[
                {
                    "value": 1, "label": "Monday"
                },
                {
                    "value": 2, "label": "Tues"
                                    },
                {
                    "value": 3, "label": "Wed"
                                    },
                {
                    "value": 4, "label": "Thur"
                                    },
                {
                    "value": 5, "label": "Fri"
                                    },
                {
                    "value": 6, "label": "Sat"
                                    },
                {
                    "value": 7, "label": "Sun"
                }
            ],
            multi=True,
            placeholder="Select certain days",
        ),
        dbc.RadioItems(
            id="day-selector-special",
            options=[
                {"label": "Weekday only", "value": 1},
                {"label": "Saturday", "value": 2},
                {"label": "Sunday", "value": 3,},
            ],
            value=[],
            inline=True,
        ),
    ]
)

slider = dbc.FormGroup(
    [
        dbc.Label("Slider", html_for="slider"),
        dcc.Slider(id="slider", min=0, max=10, step=0.5, value=3),
    ]
)

range_slider = dbc.FormGroup(
    [
        dbc.Label("RangeSlider", html_for="range-slider"),
        dcc.RangeSlider(id="range-slider", min=0, max=23, value=[6, 8], 
        marks={i: str(i) for i in range(0, 24)},
                            ),
    ]
)

form = dbc.Form([route_selector, route_direction, date_range, time_range, day_range])