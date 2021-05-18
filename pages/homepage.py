import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def homepage_body(logo_src):
    body = dbc.Container(
        [
            dbc.Row([
                # Column for app info
                dbc.Col(
                    [
                        html.Div(
                            # className="columns div-user-controls",
                            children=[
                                html.Img(className="logo",
                                          src=logo_src
                                              ),
                                html.H2("NYCBUSWATCHER VIEWER"),
                            ]
                        ),

                        html.Div(children=[
                                  html.P("""This visualization shows data analysis on observed bus positions on 4 routes
                                                      serving the East 149th Street corridor in the Bronx."""
                                    ),
                                  html.P("""The MainPage shows bus position and travel speed on an animated map,
                                                      and three bus service quality metrics on heatmap graphs.
                                                      The data will be filtered through selecting different options on 
                                                      the control panel on the top left side of the webpage. 
                                                      The panel also provide hourly aggregation options
                                                      for the heatmap graphs."""
                                    ),
                                  html.P("""The Appendix page shows the bus position data on a histogram and a map. 
                                                      It supports filters for user specific data.
                                                      The page also shows all the bus stops in Bronx in a static map."""
                                    ),
                                  dcc.Markdown(children=[
                                      "Source: [Cornell Tech Urban Tech Hub]("
                                      "https://github.com/Cornell-Tech-Urban-Tech-Hub)"
                                  ])
                              ]
                        )
                    ],
                    className=
                    'row col-lg-6 col-md-6 col-xs-12 col-sm-12',
                    style={'padding': '30px 30px 10px 50px'},
                ),
            ])
        ],
        className="mt-4",
    )
    return body


def Homepage(logo_src):
    layout = html.Div(homepage_body(logo_src))
    return layout