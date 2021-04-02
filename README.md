# NYC Buswatcher Data Viewer

## About this app

This is a demo of the Dash interactive Python framework developed by [Plotly](https://plot.ly/).

## How to run this app

(The following instructions apply to Windows command line.)

To run this app first clone repository and then open a terminal to the app folder.

```
git clone https://github.com/anthonymobile/bus_dash_2
cd bus_dash_2
```

Create and activate a new virtual environment (recommended) by running
the following:


```bash
python3 -m venv myvenv
# source myvenv/bin/activate
cd myvenv
activate
cd ..
```

Install the requirements:

```
pip install -r requirements.txt
```

Put `feb2021e149th.csv` file in the root folder

Set environement variable:  
Windows:
```
set MAPBOX_API_KEY=<your map box access token>
```
Linux:
```
export MAPBOX_API_KEY=<your map box access token>
```

Run the app:

```
python app.py
```
You can run the app on your browser at http://127.0.0.1:8050




## Source

Adapted from Dash sample app ["Uber Rides"](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-uber-rides-demo).