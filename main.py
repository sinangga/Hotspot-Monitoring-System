# Import Libraries
import pandas as pd
import geopandas
import folium
import geodatasets
import streamlit as st
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

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


# OpenStreetMap
#map = folium.Map(location=[-.5, 111.5], tiles="OpenStreetMap", zoom_start=8)
# Iterate through list and add a marker for each volcano, color-coded by its type.

#map


#st_data = st_folium(map, width=700)


def create_map():
    if 'map' not in st.session_state or st.session_state.map is None:
        m = folium.Map(location=[-.5, 111.5], tiles="OpenStreetMap", zoom_start=8)
        
        #marker_cluster = MarkerCluster().add_to(m)
        #folium.Marker(location=[45.372, -121.6972], popup="Mt. Hood Meadows").add_to(marker_cluster)
        i = 0
        for coordinates in geo_df_list:
            url = "https://maps.google.com/?ll="+str(geo_df_list[i][0])+","+str(geo_df_list[i][1])
            m.add_child(
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
                    + st.link_button("Direction",url),
                    #+ "<a href={url}><button style="backgroundcolor:GreenYellow;">Get Direction</button></a>",
                    icon=folium.Icon(),
                )
            )
            i = i + 1
        
        st.session_state.map = m  # Save the map in the session state
    return st.session_state.map

def show_map():
    m = create_map()  # Get or create the map
    folium_static(m)

show_map()
