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
                                  html.
                                  P("""This visualization shows observed bus positions on 4 routes
                                                      serving the East 149th Street corridor in the Bronx.
                                                      Select different days using the date picker or by
                                                      selecting different time frames on the histogram."""
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