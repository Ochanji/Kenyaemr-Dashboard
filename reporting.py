import streamlit as st
import pandas as pd

from dataset import df_hts as hts
from dataset import df_ct as ct

def app():
##################################################################################################################################
    st.title("HTS reporting template")

    Year = st.multiselect(
        'Select Year',
        options=hts['Year'].unique(),
        default=hts['Year'].unique())

    Month = st.multiselect(
        'Select Month',
        options=hts['Month'].unique(),
        default=hts['Month'].unique())

    KeyPopulationType = st.multiselect(
        'Select Key Population Type',
        options=hts['KeyPopulationType'].unique(),
        default=hts['KeyPopulationType'].unique())

    Gender = st.multiselect(
        'Select Gender',
        options=hts['Gender'].unique(),
        default=hts['Gender'].unique())

    Strategy = st.multiselect(
        'Select Strategy',
        options=hts['Strategy'].unique(),
        default=hts['Strategy'].unique())

    HTSResult = st.multiselect(
        'Select HTS Result',
        options=hts['HTSResult'].unique(),
        default=hts['HTSResult'].unique())

    LinkageStatus = st.multiselect(
        'Select Linkage Status',
        options=hts['LinkageStatus'].unique(),
        default=hts['LinkageStatus'].unique())

    hts_selections = hts.query(
        "Gender == @Gender & Month == @Month & Year == @Year & LinkageStatus == @LinkageStatus & HTSResult == @HTSResult & Strategy == @Strategy & KeyPopulationType == @KeyPopulationType")

    st.table(pd.crosstab(index=hts_selections['HTSResult'],
                         margins=True, columns=[hts_selections['AgeGroup'], hts_selections['Gender']]))


####################################################################################################################################
    st.title("Care & Treament reporting template")



    st.table(pd.crosstab(index='count', margins=True, columns=[
             ct['AgeGroup'], ct['Gender']]))