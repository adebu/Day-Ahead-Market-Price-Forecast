import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import geojson
import pandas as pd

# Load GeoJSON data
with open("app/available_countries.geojson", "r", encoding="utf-8") as f:
    geometry = geojson.load(f)

# Sample data (replace with your own)


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='choropleth-map')
])



if __name__ == '__main__':
    app.run_server(debug=True)
