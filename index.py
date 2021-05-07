import dash
import dash_html_components as html
from dash.dependencies import Input, Output

# from pages.positions import Position
from pages.mainpage import MainPage
from pages.appendix import Appendix
from pages.homepage import Homepage
from pages.tabsbar import Tabsbar

from app import app

tabs = Tabsbar()
app.layout = tabs

@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "about":
        return Homepage(app.get_asset_url("cornell-logo.png"))
    # elif at == "positions":
    #     return Position()
    elif at == "mainpage":
        return MainPage()
    elif at == "appendix":
        return Appendix()
    return html.P("This shouldn't ever be displayed...")

if __name__ == '__main__':
    app.run_server(debug=True)