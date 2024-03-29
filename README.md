# NYC Buswatcher Data Viewer

## About this app

This is a visualization app demonstrating data analysis on observed bus positions on 4 routes serving the East 149th Street corridor in the Bronx. It uses the Dash interactive Python framework developed by [Plotly](https://plot.ly/).

## How to run this app

(The following instructions apply to Windows command line.)

To run this app first clone repository and then open a terminal to the app folder.

```
git clone https://github.com/Jamie-Jay/bus_dash_2
cd bus_dash_2
```

Create and activate a new virtual environment (recommended) by running
the following:


```bash
python3 -m venv myvenv
# source myvenv/bin/activate # Linux
cd myvenv
activate
cd ..
```

Install the requirements:

```
pip install -r requirements.txt
```

<!-- Put `feb2021e149th.csv` file in the data folder -->
Put `feb2021e149th_Bx19_processed.csv` file in the `./data` folder

<!-- Set environement variable:  
Windows:
```
set MAPBOX_API_KEY=<your map box access token>
```
Linux:
```
export MAPBOX_API_KEY=<your map box access token>
``` -->

Run the app:
<!-- 1. Simulate backend data:
- Create geojson for bus stops:
```
python data/creategeojson.py
```
2. Run: -->
```
python index.py
```
You can run the app on your browser at http://127.0.0.1:8050




## Source

Adapted from Dash sample app ["Uber Rides"](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-uber-rides-demo).