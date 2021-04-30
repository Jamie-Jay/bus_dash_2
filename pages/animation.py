import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

import sys
sys.path.append('../')
import components.controls as controls
import components.shows as shows
import components.controls2 as controls2

def Animation():
    # Layout of Dash App
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        # Column for map
                        [# Column for app graphs and plots
                            dbc.Row(
                            [
                                dbc.Col(
                                  dbc.Label("Animated Map"),
                                )
                            ]),
                            dbc.Row(
                            [
                                dbc.Col([
                                  controls2.route_selector, 
                                ],
                                className='col-4'
                                ),
                                dbc.Col([
                                  controls2.route_direction,
                                ],
                                className='col-4'
                                )
                            ]),
                            dbc.Row(
                            [
                                dbc.Col(
                                    controls2.time_range,
                                )
                            ]),
                            dbc.Row(
                            [
                                dbc.Col(
                                    controls.date_picker_comp(),
                                )
                            ]),
                            dbc.Row(
                            [
                                dbc.Col(
                                    shows.show_mapbox_animated()
                                )
                            ])
                        ],
                    ),
                ]
            ),
        ]
    )
    return layout