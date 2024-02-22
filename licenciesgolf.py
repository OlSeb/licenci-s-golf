import pandas as pd
# import plotly
import geopandas as gpd
import plotly.graph_objects as go
import json
import streamlit as st

df = pd.read_excel("Licenciés golf.xlsx")
df.columns = ['code', 'département', 'licenciés']
df['code'] = df['code'].astype('object')

# Split Corse in 2
df['département'] = df['département'].replace('Corse', 'Corse-du-Sud')
df['code'] = df['code'].replace("20", '2A')

# Add 2nd Corse
new_row = {'département': 'Haute-Corse', 'code': '2B', "licenciés": 1793}
df.iloc[95] = new_row

# Change code (1,2,3..) to (01,02,03...) to match geojson file
df['code'] = df['code'].astype(str).str.zfill(2)

# Import geojson for geometry
sf = gpd.read_file('departements-version-simplifiee.geojson')
sf.columns = ['code', 'département', 'geometry']
sf['code'] = sf['code'].astype('object')

# Merge both df
merged_df = sf.merge(df[['code', 'licenciés']], on='code', how='left')
merged_df.fillna(1793, inplace=True)

geojson_file_path = 'departements-version-simplifiee.geojson'

# Load the GeoJSON file
with open(geojson_file_path, 'r') as file:
    france_geojson = json.load(file)

fig = go.Figure(go.Choroplethmapbox(
    geojson=france_geojson,  # Your loaded GeoJSON for France
    locations=merged_df['code'],  # The identifiers in your data that match features in the GeoJSON
    z=merged_df['licenciés'],  # The numerical values you want to display
    featureidkey="properties.code",
    colorscale="OrRd",  
    text=merged_df['département'],
    zmin=min(merged_df['licenciés']),  # Optional: set the minimum of your color scale
    zmax=max(merged_df['licenciés']),  # Optional: set the maximum of your color scale
    marker_opacity=1,  # Optional: set the opacity of the choropleth
    marker_line_width=1,  # Optional: set the width of the borders between regions
    marker_line_color='white', # line markers between states
    colorbar_title="Licenciés Golf",
))

# Set the map to be centered on France
fig.update_layout(mapbox_style="white-bg", 
                  mapbox_zoom=4.9, 
                  mapbox_center={"lat": 46.5, "lon": 2.2137})

fig.update_layout(
    title={
        'text': "Licenciés Golf par Département",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    width=1000,  # Set the width of the figure
    height=800,  # Set the height of the figure
    autosize=False  # Disable autosizing to use the specified width and height
)

# fig.show()

st.plotly_chart(fig)