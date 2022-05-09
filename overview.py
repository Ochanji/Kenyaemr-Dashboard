
import pandas as pd
import streamlit as st
import plotly.express as px


from dataset import df_overview


def app():
    column1, column2 = st.columns(2)
    with column1:
        st.markdown(
            "Chart 2"
        )
        st.plotly_chart(
            px.histogram(
                data_frame=df_overview,
                x='KPType',
                text_auto=True,
                color='Program'
            ), use_container_width=True
        )

        st.table(
            pd.crosstab(
                index=df_overview['KPType'],
                columns=df_overview['Program'],
            )
        )

        st.plotly_chart(
            px.pie(
                data_frame=df_overview,
                names='KPType'
            ), use_container_width=True
        )

    with column2:
        st.markdown(
            "Chart 2"
        )
        st.plotly_chart(
            px.histogram(
                data_frame=df_overview,
                x='AgeGroup',
                category_orders={
                    'AgeGroup': ['14yrs & below', '15-17yrs', '18-19yrs', '20-24yrs',
                                 '25-29yrs', '30-34yrs', '35-39yrs', '40-44yrs', '45-49yrs', '50+yrs']
                },
                color='KPType',
            ), use_container_width=True
        )

        st.table(
            pd.crosstab(
                index=df_overview['KPType'],
                columns='count'
            )
        )

        st.plotly_chart(
            px.pie(
                data_frame=df_overview,
                names='KPType'
            ), use_container_width=True
        )
