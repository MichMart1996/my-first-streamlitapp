import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


st.title("MPG")
df_mpg = pd.read_csv("data/mpg.csv")

if st.sidebar.checkbox('Show dataframe'):
    st.header("dataframe")
    st.dataframe(df_mpg.head(10))

show_plot = st.sidebar.radio(
    label='Choose Scatter Plot type', options=['Matplotlib', 'Plotly'])

show_means = st.sidebar.radio(
    label='Show class means', options=['Yes', 'No'])

mpg_years = ['All']
mpg_years.extend(list(df_mpg.groupby('year', as_index=False)['hwy'].count()['year']))
mpg_year = st.sidebar.selectbox("Choose a Year", mpg_years)

mpg_classes = ['All']
mpg_classes.extend(list(df_mpg.groupby('class', as_index=False)['hwy'].count()['class']))
mpg_class = st.sidebar.selectbox("Choose a Class", mpg_classes)


def scatter(show_plot, mpg_year, mpg_class):
    group = df_mpg.sort_values(by='class')
    if mpg_year != 'All' and mpg_class != 'All':
        group = df_mpg[(df_mpg['year'] == mpg_year) & (df_mpg['class'] == mpg_class)]
    elif mpg_year != 'All':
        group = df_mpg[df_mpg['year'] == mpg_year]
    elif mpg_class != 'All':
        group = df_mpg[df_mpg['class'] == mpg_class]
    
    if show_plot == 'Matplotlib':
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.margins(0.05)
        ax.set_title("Highway Fuel Efficiency")
        ax.set_xlabel("hwy")
        ax.set_ylabel("displ")
        ax.set_xlim(10, 45)
        ax.set_ylim(1, 7)

        sns.scatterplot(
            x="hwy",
            y="displ",
            data=group.sort_values(by='class'),
            hue='class'
        )
        ax.legend()

        return fig
    else:
        fig_mpg_scatter = px.scatter(group, x='hwy', y='displ', range_x=[10, 45], range_y=[1, 7], opacity=0.5, title='Highway Fuel Efficiency', color=group['class'])

        return fig_mpg_scatter


def scatter_mean(show_plot):
    group_means = df_mpg.sort_values(by='class').groupby('class', as_index=False)[['hwy', 'displ']].mean()

    if show_plot == 'Matplotlib':
        fig_means, ax_means = plt.subplots(figsize=(10, 8))
        ax_means.margins(0.05)
        ax_means.set_title("Highway Fuel Efficiency Means")
        ax_means.set_xlabel("hwy")
        ax_means.set_ylabel("displ")
        ax_means.set_xlim(10, 45)
        ax_means.set_ylim(1, 7)

        sns.scatterplot(
            x="hwy",
            y="displ",
            data=group_means.sort_values(by='class'),
            hue='class'
        )
        ax_means.legend()

        return fig_means
    else:
        fig_mpg_scatter_mean = px.scatter(group_means, x='hwy', y='displ', range_x=[10, 45], range_y=[1, 7], opacity=0.5, title='Highway Fuel Efficiency Means', color=group_means['class'])

        return fig_mpg_scatter_mean


if show_plot == 'Matplotlib' and mpg_year and mpg_class:
    st.pyplot(scatter(show_plot, mpg_year, mpg_class))
elif show_plot == 'Matplotlib':
    st.pyplot(scatter(show_plot, 'All', 'All'))
elif show_plot == 'Plotly' and mpg_year and mpg_class:
    st.plotly_chart(scatter(show_plot, mpg_year, mpg_class))
else:
    st.plotly_chart(scatter(show_plot, 'All', 'All'))

if show_plot == 'Matplotlib' and show_means == 'Yes':
    st.pyplot(scatter_mean(show_plot))
elif show_means == 'Yes':
    st.plotly_chart(scatter_mean(show_plot))