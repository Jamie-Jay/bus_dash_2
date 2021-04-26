import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import sys
sys.path.append('../')
import components.controls as controls
import components.shows as shows


def Position():
    # Layout of Dash App
    layout = html.Div(
        [
            dbc.Row(
                # Column for user controls
                [
                    dbc.Col(
                        [
                            controls.date_picker_comp(),
                            controls.hour_selector_comp()
                        ],
                        # className='col-lg-6 col-md-6 col-xs-12 col-sm-12',
                        style={'padding': '20px 20px 10px 20px'}
                    ),
                    dbc.Col(
                        [
                            controls.route_selector_comp(),
                        ],
                        # className='col-lg-6 col-md-6 col-xs-12 col-sm-12',
                        style={'padding': '20px 20px 10px 20px'}
                    ),
                    dbc.Col(
                        shows.show_position_stat(),
                        # className='col-lg-6 col-md-6 col-xs-12 col-sm-12',
                        style={'padding': '20px 20px 10px 20px'}
                    ),
                ],
                # className='col-lg-6 col-md-12 col-xs-12 col-sm-12'
            ),

            # graphs
            dbc.Row(
                [
                    dbc.Col(
                        [
                            shows.show_histogram()
                        ],
                        className='col-lg-6 col-md-12 col-xs-12 col-sm-12',
                        style={"margin": '0px', 'padding':'0px'}
                    ),
                    dbc.Col(
                        [# Column for app graphs and plots
                            shows.show_mapbox()
                        ],
                        className='col-lg-6 col-md-12 col-xs-12 col-sm-12',
                        style={"margin": '0px', 'padding':'0px'}
                    )
                ],
                className="row-same-height"
            )
        ]
    )
    return layout