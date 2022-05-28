from email import header
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
TST_Target = 5582
POS_Target = 76


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
    
    KP = df_hts_selections[df_hts_selections['PopulationType'] == 'KeyPopulation']

    TST_Achievement_Neg = int(len(KP[KP['HTSResult'] == 'Negative']['First Name']))
    TST_Achievement_Pos = int(len(KP[KP['HTSResult'] == 'Positive']['First Name']))

    TST_Proportion = round(((TST_Achievement_Neg/TST_Target)*100),1)
    Pos_Proportion = round(((TST_Achievement_Pos/POS_Target)*100),1)
    
    hed1, hed2 = st.columns(2)

    with hed1:
        st.markdown(f"###### HTS_TST Target: {TST_Target}")
        st.markdown(f"###### HTS_POS Target: {POS_Target}")
    with hed2:
        st.markdown(f"###### HTS_TST Achievement {TST_Achievement_Neg} ({TST_Proportion}%)")
        st.markdown(f"###### HTS_POS Achievement {TST_Achievement_Pos} ({Pos_Proportion}%)")

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
                x='Provider',
                color='HTSResult',
                text_auto=True,
                category_orders={'HTSResult':['Negative','Positive']}
            ), use_container_width=True
        )
    with m2:
        st.plotly_chart(
            px.histogram(
                data_frame=df_hts_month,
                x='Provider',
                color='PopulationType',
                text_auto=True,
                category_orders={'PopulationType':['KeyPopulation','General Population']}
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

