# Import Libraries
import pandas as pd
import geopandas
import folium
import geodatasets
import matplotlib.pyplot as plt
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import st_folium

## FOLIUM MAPPING


# Let's set your map key that was emailed to you. It should look something like 'abcdef1234567890abcdef1234567890'
MAP_KEY = 'c3d37be8d94206e3181b95791f4b6aad'
idn_url = 'https://firms.modaps.eosdis.nasa.gov/api/country/csv/' + MAP_KEY + '/MODIS_NRT/IDN/2'
df_idn = pd.read_csv(idn_url)

geometry = geopandas.points_from_xy(df_idn.longitude, df_idn.latitude)
geo_df = geopandas.GeoDataFrame(
    df_idn[["country_id","latitude","longitude","brightness","scan","track","acq_date","acq_time","satellite","instrument","confidence","version","bright_t31","frp","daynight"]], geometry=geometry
)
# Create a geometry list from the GeoDataFrame
geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry]

# Iterate through list and add a marker for each volcano, color-coded by its type.
i = 0
for coordinates in geo_df_list:
    # assign a color marker for the type of volcano, Strato being the most common
    # Place the markers with the popup labels and data
    map.add_child(
        folium.Marker(
            location=coordinates,
            popup="Satellite: "
            + str(geo_df.satellite[i])
            + "<br>"
            + "Date: "
            + str(geo_df.acq_date[i])
            + "<br>"
            + "Confidence: "
            + str(geo_df.confidence[i])
            + "<br>"
            + "Coordinates: "
            + str(geo_df_list[i])
            + "<br>"
            + "<a href=https://www.google.com/maps/search/?api=1&query="+str(geo_df_list[i][0])+","+str(geo_df_list[i][1])+">Get Direction</a>",
            icon=folium.Icon(),
        )
    )
    i = i + 1
# map
# OpenStreetMap
map = folium.Map(location=[-.5, 111.5], tiles="OpenStreetMap", zoom_start=8)

st_data = st_folium(map)
