import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


st.title("Volcanoes")
countries = px.choropleth()
df_volcanoes = pd.read_csv("data/volcano_ds_pop.csv")
df_volcanoes = df_volcanoes.drop("Unnamed: 0", axis="columns")

if st.sidebar.checkbox('Show dataframe'):
    st.header("dataframe")
    st.dataframe(df_volcanoes)

show_plot = st.sidebar.radio(
    label='Choose Scatter Plot type', options=['Longitude/Latitude', 'Elevation/Population (2020)'])

elev = [(-10000, 20000), (-10000, 0), (0, 1000), (1000, 2000), (2000, 3000), (3000, 4000), (4000, 5000), (5000, 20000)]

def plotly(elev_option):
    group = df_volcanoes[(df_volcanoes["Elev"] >= elev[elev_option][0]) & (df_volcanoes["Elev"] < elev[elev_option][1])]
    fig_volcanoes = go.Figure(
        data=go.Scattergeo(
            lon = group['Longitude'],
            lat = group['Latitude'],
            text = group['Type'],
            mode = 'markers',
            marker_color = group['Elev'],
            marker_size = 10,
            opacity = 1
        )
    )

    fig_volcanoes.update_layout(mapbox_style="carto-positron", mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    fig_volcanoes.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig_volcanoes


def scatter(scatter_option):
    if scatter_option == 0:
        fig_volcanoes_scatter = px.scatter(df_volcanoes, x='Longitude', y='Latitude', opacity=0.5, title='Longitude and Latitude', color=df_volcanoes['Type'])
    elif scatter_option == 1:
        fig_volcanoes_scatter = px.scatter(df_volcanoes, x='Elev', y='Population (2020)', range_y=[0, 500000000], opacity=0.5, title='Elevation and Population (2020)', color=df_volcanoes['Type'])

    return fig_volcanoes_scatter


elev_classes = ["All", "0-", "0-1000", "1000-2000", "2000-3000", "3000-4000", "4000-5000", "5000+"]
elev_class = st.sidebar.selectbox("Choose an Elevation", elev_classes)

st.plotly_chart(plotly(elev_classes.index(elev_class)))

if show_plot == 'Longitude/Latitude':
    st.plotly_chart(scatter(0))
else:
    st.plotly_chart(scatter(1))