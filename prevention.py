from dataset import df_prevention
import pandas as pd
import streamlit as st
import plotly.express as px


def app():
    st.title(':bar_chart: Prevention Dashboard')
    st.dataframe(df_prevention)

    df_prevention.to_csv('C:/Users/Ochanji/Desktop/cv.csv')