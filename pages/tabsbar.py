import dash_bootstrap_components as dbc
import dash_html_components as html

def Tabsbar():
    tabs = html.Div(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(label="About", tab_id="about"),
                            # dbc.Tab(label="Bus Positions", tab_id="positions"),
                            dbc.Tab(label="MainPage", tab_id="mainpage"),
                            dbc.Tab(label="Appendix", tab_id="appendix"),
                        ],
                        id="tabs",
                        active_tab="about",
                    ),
                    html.Div(id="content"),
                ]
            )
    return tabs
