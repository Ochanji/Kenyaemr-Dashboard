from numpy import cumsum
import pandas as pd
import streamlit as st
import plotly.express as px
from dataset import df_hts

df_hts['Month'] = pd.Categorical(df_hts['Month'], categories=['October', 'November', 'December', 
                                        'January','February','March',
                                        'April','May','June',
                                        'July','August','September'])
df_hts['HTSResust'] = pd.Categorical(df_hts['HTSResult'], categories=['Negative', 'Positive'])


def app():
    st.markdown('#### :bar_chart: HTS Dashboard')

    st.markdown('------------------------------------')
    Financial_Year = st.multiselect(
        'Select Year',
        options=df_hts['Financial_Year'].unique(),
        default=df_hts['Financial_Year'].iloc[-1]
    )

    df_hts_selections = df_hts.query(
        "Financial_Year == @Financial_Year")

    st.plotly_chart(
        px.line(
            pd.crosstab(
                index=df_hts_selections['Month'],
                columns=df_hts_selections['HTSResult']
            ),
            markers=True,
            text='HTSResult'
        ).update_traces(texttemplate="%{y}"),
        use_container_width=True
    )
    col1, col2 = st.columns(2)  
    with col1:
        st.plotly_chart(
            px.histogram(
                data_frame=df_hts_selections,
                x='Month', 
                title='Monthly HTS_TST Achievement',
                text_auto=True,
                color='HTSResult',
                category_orders={'Month':['October', 'November', 'December', 
                                        'January','February','March',
                                        'April','May','June',
                                        'July','August','September']}
            ), use_container_width=True
        )
        st.plotly_chart(
            px.histogram(
                data_frame=df_hts_selections[df_hts_selections['PopulationType'] == 'KeyPopulation'],
                x='Month',
                title='Monthly HTS_TST (KP) Achievement',
                text_auto=True,
                color='HTSResult',
                category_orders={'Month':['October', 'November', 'December', 
                                        'January','February','March',
                                        'April','May','June',
                                        'July','August','September']}
            ),use_container_width=True
        )

    st.markdown('------------------------------------')
    with col2:        
        st.plotly_chart(
            px.line(
                pd.crosstab(
                index=df_hts_selections['Month'],
                columns=df_hts_selections['HTSResult']
                ).cumsum(),
                markers=True,
                text='HTSResult',
                title='Cumulative HTS_TST Achievement'
            ).update_traces(texttemplate="%{y}"), 
            use_container_width=True
        )

        st.plotly_chart(
            px.line(
                pd.crosstab(
                    index=df_hts_selections[df_hts_selections['PopulationType'] == 'KeyPopulation']['Month'],
                    columns=df_hts_selections['HTSResult']
                ).cumsum(),
                markers=True,
                text='HTSResult',
                title='Cumulative HTS_TST (KP) Achievement'
            ).update_traces(texttemplate="%{y}"), 
            use_container_width=True
        )

    st.markdown('------------------------------------')

    st.markdown('------------------------------------')

    Month = st.multiselect(
        'Month',
        options=df_hts_selections['Month'].unique(),
        default=df_hts_selections['Month'].iloc[-1]
    )

    df_hts_month = df_hts_selections.query(
        "Month == @Month")

    st.markdown('------------------------------------')

    m1, m2 = st.columns(2)
    with m1:
        st.plotly_chart(
            px.histogram(
                data_frame=df_hts_month,
                y='Provider',
                color='HTSResult',
                text_auto=True
            ), use_container_width=True
        )
    with m2:
        st.plotly_chart(
            px.histogram(
                data_frame=df_hts_month,
                y='Provider',
                color='PopulationType',
                text_auto=True
            ), use_container_width=True
        )


    st.markdown('------------------------------------')


    # st.plotly_chart(
    #     px.line(
    #         pd.crosstab(
    #             index=[df_hts_selections_Month['Date'],df_hts_selections_Month['HTSResult']]
    #         )
    #     )
    # )


    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df_hts_selections)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='HTS Linelist extract.csv',
        mime='text/csv',
    )
    st.dataframe(df_hts_selections)

