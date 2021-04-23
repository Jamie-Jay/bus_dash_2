import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from datafeed import totalList as totalList

def date_picker_comp():
    return html.Div(
        className="div-for-dropdown",
        children=[
            dcc.DatePickerSingle(
                id="date-picker",
                min_date_allowed=dt(2021, 2, 1),
                max_date_allowed=dt(2021, 2, 28),
                initial_visible_month=dt(2021, 2, 1),
                date=dt(2021, 2, 14).date(),
                display_format="MMMM D, YYYY",
                style={"border": "0px solid black"},
            )
        ],
    )

def route_selector_comp():
    return html.Div(
        className="div-for-dropdown",
        children=[
            # Dropdown for route on map
            dcc.Dropdown(
                id="route-selector",
                options=[
                    {
                        "label": route,
                        "value": route
                    }
                    for route in totalList.keys()
                ],
                placeholder="Select a route",
                value=list(totalList.keys())[0],
                multi=True
            )
        ],
    )
    
def hour_selector_comp():
    return html.Div(
        className="div-for-dropdown",
        children=[
            # Dropdown to select times
            dcc.Dropdown(
                id="hour-selector",
                options=[
                    {
                        "label": str(n) + ":00",
                        "value": str(n),
                    }
                    for n in range(24)
                ],
                multi=True,
                placeholder="Select certain hours",
            )
        ],
    )

# # Selected Data in the Histogram updates the Values in the Hours selection dropdown menu
# @app.callback(
#     Output("hour-selector", "value"),
#     [Input("histogram", "selectedData"), Input("histogram", "clickData")],
# )
def update_hour_selector(value, clickData):
    holder = []
    if clickData:
        holder.append(str(int(clickData["points"][0]["x"])))
    if value:
        for x in value["points"]:
            holder.append(str(int(x["x"])))
    return list(set(holder))


# # Clear Selected Data if Click Data is used
# @app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
def update_selected_data(clickData):
    if clickData:
        return {"points": []}


# # Update the total number of positions Tag
# @app.callback(Output("total-positions", "children"), [Input("date-picker", "date")])
def update_total_positions(datePicked):
    date_picked = dt.strptime(datePicked, "%Y-%m-%d")

    total_pos = 0
    for value in totalList.values():
        total_pos += len(value[date_picked.month - 4][date_picked.day - 1])
    return "Total Number of bus positions: {:,d}".format(
        total_pos
    )


# Select all routes when no routes are selected
def update_routes(routeSelected):
    if (routeSelected == None or len(routeSelected) == 0):
        routeSelected = list(totalList.keys())
    if isinstance(routeSelected, str):
        routeSelected = [routeSelected]

    return routeSelected

# # Update the total number of positions in selected times
# @app.callback(
#     [Output("total-positions-selection", "children"), Output("date-value", "children")],
#     [Input("route-selector", "value"), Input("date-picker", "date"), Input("hour-selector", "value")],
# )
def update_total_positions_selection(routeSelected, datePicked, selection):
    firstOutput = ""

    if selection != None or len(selection) != 0:
        date_picked = dt.strptime(datePicked, "%Y-%m-%d")
        totalInSelection = 0

        routeSelected = update_routes(routeSelected)
        for r in routeSelected:
            for x in selection:
                totalInSelection += len(
                    totalList[r][date_picked.month - 4][date_picked.day - 1][
                        totalList[r][date_picked.month - 4][date_picked.day - 1].index.hour
                        == int(x)
                    ]
                )
        firstOutput = "Total positions in selection: {:,d}".format(totalInSelection)

    if (
        datePicked == None
        or selection == None
        or len(selection) == 24
        or len(selection) == 0
        or routeSelected == None
        or len(routeSelected) == 0
    ):
        return firstOutput, (datePicked, " - showing hour(s): All")

    holder = sorted([int(x) for x in selection])

    if holder == list(range(min(holder), max(holder) + 1)):
        return (
            firstOutput,
            (
                datePicked,
                " - showing hour(s): ",
                holder[0],
                "-",
                holder[len(holder) - 1],
            ),
        )

    holder_to_string = ", ".join(str(x) for x in holder)
    return firstOutput, (datePicked, " - showing hour(s): ", holder_to_string)