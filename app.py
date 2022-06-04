# %%
import streamlit as st
import pandas as pd
import plotly.express as px

# %%
from dataset import df_overview
from dataset import df_hts
from dataset import df_ct
from dataset import df_prevention

# %%
df_hts['Month'] = pd.Categorical(
    values= df_hts['Month'],
    categories=['October', 'November', 'December',
                'January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'August', 'September'])

df_hts['HTSResust'] = pd.Categorical(
    values= df_hts['HTSResult'], 
    categories=['Negative', 'Positive'])

df_prevention['Month'] = pd.Categorical(
    values=df_prevention['Month'],
    categories=['October', 'November', 'December',
                'January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'August', 'September'])

df_ct['Month'] = pd.Categorical(
    values=df_ct['Month'],
    categories=['October', 'November', 'December',
                'January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'August', 'September'])

df_ct['Last Visit Month'] = pd.Categorical(
    values=df_ct['Last Visit Month'],
    categories=['October', 'November', 'December',
                'January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'August', 'September'])

# %%
HTS_TST_TARGET = 5582
HTS_TST_POS_TARGET = 76
KP_PREV_FSW = 4152
KP_PREV_MSM = 2400
GEND_GBV_KP = 1405
TX_CURR_KP = 764
TX_NEW_KP = 72
CxCa_KP = 191

# %%
st.set_page_config(
    layout='wide',
    page_title='Performance Dashboard',
    page_icon=':bar_chart:',
    initial_sidebar_state='collapsed'
)

def page2():
    st.markdown('##### HIV Testing Services')
    Financial_Year = st.multiselect(
        'Select Year',
        options=df_hts['Financial_Year'].unique(),
        default=df_hts['Financial_Year'].iloc[-1]
    )

    df_hts_selections = df_hts.query(
        "Financial_Year == @Financial_Year")

    KP = df_hts_selections[df_hts_selections['PopulationType']
                           == 'KeyPopulation']

    TST_Achievement_Neg = int(
        len(KP[KP['HTSResult'] == 'Negative']['First Name']))
    TST_Achievement_Pos = int(
        len(KP[KP['HTSResult'] == 'Positive']['First Name']))

    TST_Proportion = round(((TST_Achievement_Neg/HTS_TST_TARGET)*100), 1)
    Pos_Proportion = round(((TST_Achievement_Pos/HTS_TST_POS_TARGET)*100), 1)

    hed1, hed2 = st.columns(2)

    with hed1:
        st.markdown(f"###### HTS_TST Target: {HTS_TST_TARGET}")
        st.markdown(f"###### HTS_POS Target: {HTS_TST_POS_TARGET}")
    with hed2:
        st.markdown(
            f"###### HTS_TST Achievement {TST_Achievement_Neg} ({TST_Proportion}%)")
        st.markdown(
            f"###### HTS_POS Achievement {TST_Achievement_Pos} ({Pos_Proportion}%)")

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
                category_orders={'Month': ['October', 'November', 'December',
                                           'January', 'February', 'March',
                                           'April', 'May', 'June',
                                           'July', 'August', 'September']}
            ), use_container_width=True
        )
        st.plotly_chart(
            px.histogram(
                data_frame=df_hts_selections[df_hts_selections['PopulationType']
                                             == 'KeyPopulation'],
                x='Month',
                title='Monthly HTS_TST (KP) Achievement',
                text_auto=True,
                color='HTSResult',
                category_orders={'Month': ['October', 'November', 'December',
                                           'January', 'February', 'March',
                                           'April', 'May', 'June',
                                           'July', 'August', 'September']}
            ), use_container_width=True
        )

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
                    index=df_hts_selections[df_hts_selections['PopulationType']
                                            == 'KeyPopulation']['Month'],
                    columns=df_hts_selections['HTSResult']
                ).cumsum(),
                markers=True,
                text='HTSResult',
                title='Cumulative HTS_TST (KP) Achievement'
            ).update_traces(texttemplate="%{y}"),
            use_container_width=True
        )

    Month = st.multiselect(
        'Month',
        options=df_hts_selections['Month'].unique(),
        default=df_hts_selections['Month'].iloc[-1]
    )

    df_hts_month = df_hts_selections.query(
        "Month == @Month")

    m1, m2 = st.columns(2)
    with m1:
        st.plotly_chart(
            px.histogram(
                data_frame=df_hts_month,
                x='Provider',
                color='HTSResult',
                text_auto=True,
                category_orders={'HTSResult': ['Negative', 'Positive']}
            ), use_container_width=True
        )
    with m2:
        st.plotly_chart(
            px.histogram(
                data_frame=df_hts_month,
                x='Provider',
                color='PopulationType',
                text_auto=True,
                category_orders={'PopulationType': [
                    'KeyPopulation', 'General Population']}
            ), use_container_width=True
        )

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


def page3():
    st.markdown("##### Prevention")
    st.markdown('#### :bar_chart: Prevention Dashboard')
    Financial_Year = st.multiselect(
        'Financial Year',
        options=df_prevention['Financial_Year'].unique(),
        default=df_prevention['Financial_Year'].iloc[-1]
    )

    df_prevention_selections = df_prevention.query(
        "Financial_Year == @Financial_Year")

    kpfsw = int(len(
        df_prevention_selections[df_prevention_selections['KPType'] == 'FSW']['First Name']))
    kpmsm = int(len(
        df_prevention_selections[df_prevention_selections['KPType'] == 'MSM']['First Name']))
    kpGEND_GBV_KP = int(len(
        df_prevention_selections[df_prevention_selections['GEND_GBV_KP'] != 'N/A']['First Name']))



    fsw = round(((kpfsw/KP_PREV_FSW)*100), 1)
    msm = round(((kpmsm/KP_PREV_MSM)*100), 1)
    p_GEND_GBV_KP = round(((kpGEND_GBV_KP/GEND_GBV_KP)*100), 1)

    hed1, hed2 = st.columns(2)
    with hed1:
        st.markdown(f"###### KP_PREV_FSW Target: {KP_PREV_FSW}")
        st.markdown(f"###### KP_PREV_FSW Target: {KP_PREV_MSM}")
        st.markdown(f"###### KP_GEND_GBV_KP Target: {GEND_GBV_KP}")
    with hed2:
        st.markdown(f"###### KP_PREV_FSW Achievement: {kpfsw} ({fsw}%)")
        st.markdown(f"###### KP_PREV_MSM Achievement: {kpmsm} ({msm}%)")
        st.markdown(f"###### KP_GEND_GBV_KP Achievement: {kpGEND_GBV_KP} ({p_GEND_GBV_KP}%)")

    st.plotly_chart(
        px.line(
            pd.crosstab(
                columns=df_prevention_selections['KPType'],
                index=df_prevention_selections['Month']
            ),
            markers=True,
            text='KPType'
        ).update_traces(texttemplate="%{y}"),
        use_container_width=True
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_selections,
                x='Month',
                color='KPType',
                text_auto=True,
                category_orders={'Month': ['October', 'November', 'December',
                                           'January', 'February', 'March',
                                           'April', 'May', 'June',
                                           'July', 'August', 'September'],
                                 'KPType': ['FSW', 'MSM', 'PWID', 'TG']}
            ), use_container_width=True
        )

    with col2:
        st.plotly_chart(
            px.line(
                pd.crosstab(
                    columns=df_prevention_selections['KPType'],
                    index=df_prevention_selections['Month']
                ).cumsum(),
                markers=True,
                text='KPType'
            ).update_traces(texttemplate="%{y}"),
            use_container_width=True
        )

    with col1:
        st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_selections[df_prevention_selections['GEND_GBV_KP'] != 'N/A'],
                x='Month',
                color='GEND_GBV_KP',
                text_auto=True
            ), use_container_width=True
        )

    with col2:
        st.plotly_chart(
            px.line(
                pd.crosstab(
                    columns=df_prevention_selections[df_prevention_selections['GEND_GBV_KP']
                                                     != 'N/A']['GEND_GBV_KP'],
                    index=df_prevention_selections[df_prevention_selections['GEND_GBV_KP']
                                                   != 'N/A']['Month']
                ).cumsum(),
                text='GEND_GBV_KP'
            ).update_traces(texttemplate="%{y}"),
            use_container_width=True
        )

    Month = st.multiselect(
        'Month',
        options=df_prevention_selections['Month'].unique(),
        default=df_prevention_selections['Month'].iloc[-1]
    )

    df_prevention_month = df_prevention_selections.query(
        "Month == @Month")
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_month,
                x='Provider',
                color='Type_Of_Visit',
                text_auto=True
            ), use_container_width=True
        )
    with col4:
        st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_month[df_prevention_month['GEND_GBV_KP'] != 'N/A'],
                x='Provider',
                color='GEND_GBV_KP',
                text_auto=True
            ), use_container_width=True
        )

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df_prevention_selections)
    st.write('Prevention Data')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='Prevention Linelist extract.csv',
        mime='text/csv',
    )
    st.dataframe(df_prevention_selections)

    # csv = convert_df(df_prep)
    # st.write('Prep Data')
    # st.download_button(
    #     label="Download data as CSV",
    #     data=csv,
    #     file_name='PrepNew Linelist extract.csv',
    #     mime='text/csv',
    # )
    # st.dataframe(df_prep)


def page4():
    st.markdown('##### Care & Treatment')

    Status = st.multiselect(
        'Select Care & Treament Status',
        options=df_ct['Status'].unique(),
        default=['On ART']
    )

    df_ct_selections = df_ct.query(
        "Status == @Status")

    Fy = df_ct_selections[df_ct_selections['Financial_Year_'] == 'Vukisha_FY1']
    Fyc = df_ct_selections[df_ct_selections['Financial_Year'] == 'Vukisha_FY1']
    ca = Fyc[Fyc['Gender'] == 'F']

    curr = len(
        df_ct_selections[df_ct_selections['PopulationType'] == 'KeyPopulation']['First Name'])
    new = len(Fy[Fy['PopulationType'] == 'KeyPopulation']['First Name'])
    cacx = len(Fyc[Fyc['CaCx'] == 'Screened']['First Name'])

    currp = round(((curr/TX_CURR_KP)*100), 1)
    newp = round(((new/TX_NEW_KP)*100), 1)
    cacxp = round(((cacx/CxCa_KP)*100), 1)

    tx_curr = len(df_ct_selections['First Name'])

    hed1, hed2 = st.columns(2)
    st.markdown(f"")
    with hed1:
        st.markdown(f"###### TX_NEW Target: {TX_NEW_KP}")
        st.markdown(f"###### TX_CURR Target: {TX_CURR_KP}")
        st.markdown(f"###### CxCa (KP) Target: {CxCa_KP}")
    with hed2:
        st.markdown(f"###### TX_NEW Achievement: {new} ({newp}%)")
        st.markdown(f"###### TX_CURR Achievement: {curr} ({currp}%)")
        st.markdown(f"###### CxCa Achievement: {cacx} ({cacxp}%)")

    st.plotly_chart(
        px.line(
            pd.crosstab(
                index=Fy['Month'],
                columns=Fy['PopulationType']
            ),
            markers=True,
            text='PopulationType'
        ).update_traces(texttemplate="%{y}"), use_container_width=True
    )
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            px.histogram(
                data_frame=Fy,
                x='Month',
                color='PopulationType',
                text_auto=True,
                category_orders={'Month': ['October', 'November', 'December',
                                           'January', 'February', 'March',
                                           'April', 'May', 'June',
                                           'July', 'August', 'September']}
            ), use_container_width=True
        )

        st.plotly_chart(
            px.histogram(
                data_frame=ca[ca['CaCx'] == 'Screened'],
                x='Last Visit Month',
                color='CaCx',
                # barmode='group',
                text_auto=True,
                category_orders={'Last Visit Month': ['October', 'November', 'December',
                                                      'January', 'February', 'March',
                                                      'April', 'May', 'June',
                                                      'July', 'August', 'September']}
            ), use_container_width=True
        )
    with col2:
        st.plotly_chart(
            px.line(
                pd.crosstab(
                    index=Fy['Month'],
                    columns=Fy['PopulationType']
                ).cumsum(),
                markers=True,
                text='PopulationType'
            ).update_traces(texttemplate="%{y}"), use_container_width=True
        )

        st.plotly_chart(
            px.line(
                pd.crosstab(
                    index=ca[ca['CaCx'] == 'Screened']['Last Visit Month'],
                    columns=ca[ca['CaCx'] == 'Screened']['CaCx']
                ).cumsum(),
                markers=True,
                text='CaCx'
            ).update_traces(texttemplate="%{y}"), use_container_width=True
        )
    col3, col4, col5 = st.columns(3)
    with col3:
        st.plotly_chart(
            px.pie(
                data_frame=df_ct_selections,
                names='VLResults',
                color='VLResults',
                title='Viral Load Results Proportions'
            ), use_container_width=True
        )
        st.table(
            pd.crosstab(
                columns=df_ct_selections['VLResults'],
                index=''
            )
        )
    with col4:
        st.plotly_chart(
            px.pie(
                data_frame=df_ct_selections,
                names='KeyPopulationType',
                color='KeyPopulationType',
                title='Key Population Proportions'
            ), use_container_width=True
        )
        st.table(
            pd.crosstab(
                columns=df_ct_selections['KeyPopulationType'],
                index=''
            )
        )

    with col5:
        st.plotly_chart(
            px.pie(
                data_frame=df_ct_selections[df_ct_selections['Gender'] == 'F'],
                names='CaCx',
                color='CaCx',
                title='Proportion Screened for CxCa'
            ), use_container_width=True
        )
        st.table(
            pd.crosstab(
                columns=df_ct_selections['CaCx'],
                index=''
            )
        )

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
def Overview():
    
    st.markdown("##### Overview")
    ov1, ov2, ov3, ov4, ov5, ov6 = st.columns(6)
    with ov1:
        st.info(f"###### KP_PREV_FSW {KP_PREV_FSW}")
    with ov2:
        st.info(f"###### KP_PREV_MSM {KP_PREV_MSM}")

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



# %%
page_names_to_funcs = {
    "Overview": Overview,
    "HIV Testing Services": page2,
    "Prevention Services": page3,
    "HIV Care & Treatment": page4
}

selected_page = st.radio("Select a page", page_names_to_funcs.keys())

page_names_to_funcs[selected_page]()
