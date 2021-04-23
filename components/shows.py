import dash
import dash_core_components as dcc
import dash_html_components as html

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

def show_mapbox_all():                                            
    return html.Div(
              className="text-padding",
              children=[
                  dcc.Graph(id="map-graph-all"),                                    
              ],
          )

def show_histogram():                                            
    return html.Div(
              className="text-padding",
              children=[
                  html.P("travel speed"),
                  dcc.Graph(id="histogram"), 
              ],
    )

def show_travel_speed():                                            
    return html.Div(
              className="text-padding",
              children=[
                  html.P("travel speed"),
                  dcc.Graph(id="histogram2"), 
              ],
    )

def show_bunching():                                            
    return html.Div(
              className="text-padding",
              children=[
                  html.P("bunching"),
                  dcc.Graph(id="heatmap"), 
              ],
    )

def show_burnchart():                                            
    return html.Div(
              className="text-padding",
              children=[
                  html.P("dwell time"),
                  dcc.Graph(id="burndownchart"), 
              ],
    )