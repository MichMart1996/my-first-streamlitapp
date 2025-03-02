import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


st.title("MPG")
df_mpg = pd.read_csv("data/mpg.csv")
#df_mpg = df_mpg.drop("Unnamed: 0", axis="columns")

if st.sidebar.checkbox('Show dataframe'):
    st.header("dataframe")
    st.dataframe(df_mpg.head(10))

show_plot = st.sidebar.radio(
    label='Choose Scatter Plot type', options=['Plotly', 'Matplotlib'])

mpg_years = ['All'].extend(list(df_mpg.groupby('year', as_index=False)['hwy'].count()['year']))
mpg_year = st.sidebar.selectbox("Choose a Year", mpg_years)

mpg_classes = ['All'].extend(list(df_mpg.groupby('class', as_index=False)['hwy'].count()['class']))
mpg_class = st.sidebar.selectbox("Choose a Class", mpg_classes)


def scatter(mpg_year, mpg_class):
    group = df_mpg
    #st.title("group: " + str(group))
    #st.title(str(mpg_year) + str(mpg_class))
    if mpg_year != 'All' and mpg_class != 'All':
        group = df_mpg[(df_mpg['year'] == mpg_year) & (df_mpg['class'] == mpg_class)]
    elif mpg_year != 'All':
        group = df_mpg[df_mpg['year'] == mpg_year]
    elif mpg_class != 'All':
        group = df_mpg[df_mpg['class'] == mpg_class]
    
    #fig_mpg = px.scatter(group, x='hwy', y='displ', opacity=0.5, title='Highway Fuel Efficiency', color='class')
    #fig_mpg.add_trace(go.Scatter(x=group['displ'], y=group['hwy'], mode="markers"))
    
    fig_mpg = go.Figure(
        data=go.Scatter(
            x = group['hwy'],
            y = group['displ'],
            text = group['class'],
            mode = 'markers',
            marker_color = group['class'],
            marker_size = 10,
            opacity = 1
        )
    )
    
    return fig_mpg


#st.plotly_chart(plotly(mpg_years.index(mpg_year)))
#st.plotly_chart(plotly(mpg_classes.index(mpg_class)))
if mpg_year and mpg_class:
    st.plotly_chart(scatter(mpg_year, mpg_class))
else:
    st.plotly_chart(scatter('All', 'All'))