import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from positions import Position
from travelspeed import TravelSpeed
from homepage import Homepage

import components.graphs as graphs
import components.controls as controls

from tabsbar import Tabsbar

tabs = Tabsbar()

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app = dash.Dash(
    __name__, 
    # meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.config.suppress_callback_exceptions = True

app.layout = tabs


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "about":
        return Homepage(app.get_asset_url("cornell-logo.png"))
    elif at == "positions":
        return Position()
    elif at == "travelspeed":
        return TravelSpeed()
    return html.P("This shouldn't ever be displayed...")


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoiamFtaWVqYXkiLCJhIjoiY2ttbW5oeG41MW1mYzJubnY4MXhmYm4zOSJ9.JvVgpcf7FpHVe-84FoHiUg"#os.getenv('MAPBOX_API_KEY')

@app.callback(
    Output("map-graph", "figure"),
    [
        Input("route-selector", "value"),
        Input("date-picker", "date"),
        # Input("time-range-slider", "value"),
        Input("hour-selector", "value"),    
    ],
)
def update_graph(datePicked, selectedData, selectedLocation):
    return graphs.update_graph(datePicked, selectedData, selectedLocation, mapbox_access_token)


@app.callback(
    Output("map-graph-all", "figure"),
    [
        Input("route-selector", "value"),
        Input("date-picker", "date"),
        # Input("time-range-slider", "value"),
        Input("hour-selector", "value"),    
    ],
)
def update_graph2(datePicked, selectedData, selectedLocation):
    return graphs.update_graph2(datePicked, selectedData, selectedLocation, mapbox_access_token)


# Update Histogram Figure based on Month, Day and Times Chosen
@app.callback(
    Output("histogram", "figure"),
    [Input("route-selector", "value"), Input("date-picker", "date"), Input("hour-selector", "value")],
)
def update_histogram(routeSelected, datePicked, selection):
    return graphs.update_histogram(routeSelected, datePicked, selection)


# Selected Data in the Histogram updates the Values in the Hours selection dropdown menu
@app.callback(
    Output("hour-selector", "value"),
    [Input("histogram", "selectedData"), Input("histogram", "clickData")],
)
def update_hour_selector(value, clickData):
    return controls.update_hour_selector(value, clickData)


# Clear Selected Data if Click Data is used
@app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
def update_selected_data(clickData):
    return controls.update_selected_data(clickData)


# Update the total number of positions Tag
@app.callback(Output("total-positions", "children"), [Input("date-picker", "date")])
def update_total_positions(datePicked):
    return controls.update_total_positions(datePicked)


# Update the total number of positions in selected times
@app.callback(
    [Output("total-positions-selection", "children"), Output("date-value", "children")],
    [Input("route-selector", "value"), Input("date-picker", "date"), Input("hour-selector", "value")],
)
def update_total_positions_selection(routeSelected, datePicked, selection):
  return controls.update_total_positions_selection(routeSelected, datePicked, selection)

if __name__ == '__main__':
    app.run_server(debug=True)