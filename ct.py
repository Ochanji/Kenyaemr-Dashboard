# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import pandas as pd
import streamlit as st
import plotly.express as px

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

from dataset import df_ct
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def app():
    st.title(
        ':bar_chart: Care & Treatment Dashboard'
    )
##########################################################################################################
    st.markdown('##')
    enroled = int(len(df_ct['First Name']))
    st.markdown(f"Total clients enrolled in HIV Program: # {enroled}")

    art = df_ct.Status.value_counts()['On ART']
    st.markdown(f"Clients currently on ART: # {art}")

    sup = int(df_ct.VLResults.value_counts()['LDL'] +
              df_ct.VLResults.value_counts()['1-400 Cpies'] +
              df_ct.VLResults.value_counts()['401 - 999 Copies'])
    st.markdown(f"Suppressed clients: # {sup}")

    usup = int(df_ct.VLResults.value_counts()['Above 1000 Copies'])
    st.markdown(f"Unsuppressed clients: # {usup}")

    st.markdown("##")
    st.sidebar.header('Filters')

    Status = st.sidebar.multiselect(
        'Select Care & Treament Status',
        options=df_ct['Status'].unique(),
        default=df_ct['Status'].unique()
    )

    Year = st.sidebar.multiselect(
        'Select Year of Enrolled',
        options=df_ct['Year'].unique(),
        default=df_ct['Year'].unique()
    )

    Month = st.sidebar.multiselect(
        'Select month of Enrolled',
        options=df_ct['Month'].unique(),
        default=df_ct['Month'].unique()
    )

    KeyPopulationType = st.sidebar.multiselect(
        'Select Key Population Type',
        options=df_ct['KeyPopulationType'].unique(),
        default=df_ct['KeyPopulationType'].unique()
    )

    VLResults = st.sidebar.multiselect(
        'Select Viral Load Results',
        options=df_ct['VLResults'].unique(),
        default=df_ct['VLResults'].unique()
    )

    Gender = st.sidebar.multiselect(
        'Select Gender',
        options=df_ct['Gender'].unique(),
        default=df_ct['Gender'].unique()
    )
    st.sidebar.markdown(
        'Note: All Filters are selected by default'
    )
    df_ct_selections = df_ct.query(
        "Status == @Status & Year == @Year & Month == @Month & KeyPopulationType == @KeyPopulationType & Gender == @Gender & VLResults == @VLResults")
##########################################################################################################
    header1, header2 = st.columns(2)
    with header1:
        st.plotly_chart(
            px.histogram(
                data_frame=df_ct_selections,
                x='AgeGroup',
                color='Gender',
                category_orders={
                    'AgeGroup': [
                        '14yrs & below', '15-17yrs', '18-19yrs', '20-24yrs', '25-29yrs', '30-34yrs', '35-39yrs', '40-44yrs', '45-49yrs', '50+yrs'
                    ]
                }
            )
        )
        st.plotly_chart(
            px.histogram(
                data_frame=df_ct_selections,
                x='KeyPopulationType',
                color='Status',
                barmode='group'
            )
        )
# -------------------------------------------------------------------------------------------------------------


##########################################################################################################

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df_ct_selections)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='C&T Lineslist extract.csv',
        mime='text/csv',
    )
    st.dataframe(df_ct_selections)
#################################################################################################################
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
