import plotly.express as px
import json

# Load GeoJSON data
with open("app/available_countries.geojson", "r", encoding="utf-8") as f:
    geometry = json.load(f)

# Create a sample DataFrame
df = {
    'GEOUNIT': ['Belgium', 'Spain', 'France'],
    'winner': [1, 2, 3]
}

# Create a choropleth map
fig = px.choropleth(df, 
                    geojson=geometry, 
                    locations="GEOUNIT", 
                    projection="mercator",
                    color="winner",
                    featureidkey="properties.GEOUNIT")

# Update the geos and layout for zoom and centering
fig.update_geos(fitbounds=False, visible=False)
fig.update_layout(
    mapbox={
        'center': {"lat": 46.603354, "lon": 1.888334},  # Center around France
        'zoom': 500000  # Adjust zoom level
    },
    margin={"r": 6, "t": 400, "l": 0, "b": 0}
)

fig.show()
