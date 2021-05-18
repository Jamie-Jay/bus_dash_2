import dash
import dash_core_components as dcc
import dash_html_components as html

import json
import numpy as np
from plotly import graph_objs as go

import data.constants as constants
import components.graphs as graphs

def show_position_stat():
    return html.Div(
      children=[
        html.P(
              "Statistics:"
          ),
        html.P(id="total-positions"),
        html.P(id="total-positions-selection"),
        html.P(id="date-value")
        ]
    )


def show_mapbox():
    return html.Div(
              className="text-padding",
              children=[
                  html.P("Scatter plot of bus positions for section data by time."),
                  dcc.Graph(id="map-graph"),                                    
              ],
          )

def show_mapbox_static():
    return html.Div(
              className="text-padding",
              children=[
                  dcc.Graph(
                      id="map-graph-static", 
                      figure=graphs.update_graph_static()
                      ),                                    
              ],
          )

def show_mapbox_animated():
    return html.Div(
              className="text-padding",
              children=[
                  dcc.Graph(
                      id="map-graph-animated", 
                    #   figure=graphs.update_graph_animated()
                      ),                                    
              ],
          )

def show_histogram():
    return html.Div(
              className="text-padding",
              children=[
                  html.P("Bus Position Count"),
                  dcc.Graph(id="histogram"), 
              ],
    )

def show_travel_speed():
    return html.Div(
              className="text-padding",
              children=[
                  html.P("HeatMap - Travel Speed (mph)"),
                  dcc.Graph(id="speedHeatMap"), 
              ],
    )

def show_bunching():
    return html.Div(
              className="text-padding",
              children=[
                  html.P("HeatMap - Bunching Count"),
                  dcc.Graph(id="bunchingHeatMap"), 
              ],
    )

def show_dwell_time():
    return html.Div(
              className="text-padding",
              children=[
                  html.P("HeatMap - If Dwelling (1 represents it is dwelling)"),
                  dcc.Graph(id="dwellingHeatMap"), 
              ],
    )