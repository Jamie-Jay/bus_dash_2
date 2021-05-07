import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

import sys
sys.path.append('../')
import components.controls as controls
import components.shows as shows
import components.controls2 as controls2
from pages.positions import Position

def Appendix():
    # Layout of Dash App
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        # Column for map
                        [
                            dbc.Label("Bus Positions", className='h3'),
                            Position(),

                            dbc.Label("Bus Stops in Bronx", className='h3'),
                            shows.show_mapbox_static()
                        ],
                    ),
                ]
            ),
        ]
    )
    return layout