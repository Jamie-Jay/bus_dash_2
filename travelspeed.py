import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import components.controls as controls
import components.shows as shows
import components.controls2 as controls2

def TravelSpeed():
    # Layout of Dash App
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        # Column for user controls
                        [
                            dbc.Label("Contol board"),
                            controls2.form
                        ],
                        # className='col-lg-6 col-md-6 col-xs-12 col-sm-12',
                        className='col-4',
                        style={'padding': '20px 20px 10px 20px'}
                    ),
                    dbc.Col(
                        # Column for map
                        [# Column for app graphs and plots
                            shows.show_mapbox_all()
                        ],
                        # className='col-lg-6 col-md-12 col-xs-12 col-sm-12',
                        className='col-8',
                        style={"margin": '0px', 'padding':'0px'}
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        # Column for travel speed
                        [
                            shows.show_travel_speed()
                        ],
                        # className='col-lg-6 col-md-12 col-xs-12 col-sm-12',
                        className='col-4',
                        style={"margin": '0px', 'padding':'0px'}
                    ),
                    dbc.Col(
                        # Column for bunching
                        [
                            shows.show_bunching()
                        ],
                        # className='col-lg-6 col-md-12 col-xs-12 col-sm-12',
                        className='col-4',
                        style={"margin": '0px', 'padding':'0px'}
                    ),
                    dbc.Col(
                        # Column for dwell time
                        [
                            shows.show_burnchart()
                        ],
                        className='col-4',
                        # className='col-lg-6 col-md-12 col-xs-12 col-sm-12',
                        style={"margin": '0px', 'padding':'0px'}
                    ),
                ]
            )
        ]
    )
    return layout