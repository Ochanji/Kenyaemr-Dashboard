# %%
import streamlit as st
import pandas as pd
import plotly.express as px

# %%
from dataset import df_overview
from dataset import df_hts
from dataset import df_ct
from dataset import df_prevention
from dataset import df_prep

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

df_prevention['Month'] = pd.Categorical(values=df_prevention['Month'],
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
df_prep['Month'] = pd.Categorical(
    values=df_prep['Month'],
    categories= ['October', 'November', 'December',
                'January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'August', 'September']
)

# %%
# HTS tarhest
HTS_TST_TARGET = 5582
HTS_TST_POS_TARGET = 76
HTS_SELF_KP = 5442
HTS_RECENT_KP = 57

# Prevention Indicators
KP_PREV_FSW = 4152
KP_PREV_MSM = 2400
GEND_GBV_KP = 1405
PrEP_NEW_KP = 1006
PrEP_CT_KP = 1409

# Care & Treatment Indicators
TX_CURR_KP = 764
TX_NEW_KP = 72
CxCa_KP = 191
TX_PVLS_D_KP = 757
TX_PVLS_N_KP = 719
TB_PREV_D_KP = 58
TB_PREV_N_KP = 52
TB_STAT_KP = 33

# %%
st.set_page_config(
    layout='wide',
    page_title='Dashboard',
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

    hed1, hed2, hed3, hed4 = st.columns(4)
    with st.container(): 
        with hed1:
            tst = f"##### HTS_TST_NEG(KP) \n##### Target: {HTS_TST_TARGET} \n##### Achievement: {TST_Achievement_Neg}({TST_Proportion}%)"
            st.info(f"{tst}")
        with hed2:
            pos = f"##### HTS_POS(KP) \n##### Target: {HTS_TST_POS_TARGET} \n##### Achievement: {TST_Achievement_Pos}({Pos_Proportion}%)"
            st.info(f"{pos}")
        with hed3:
            self = f"##### HTS_SELF(KP) \n##### Target: {HTS_SELF_KP} \n##### Achievement: "
            st.info(f"{self}")
        with hed4:
            recent = f"##### HTS_RECENT(KP) \n##### Target: {HTS_RECENT_KP} \n##### Achievement: "
            st.info(f"{recent}")
    
    st.plotly_chart(
        px.line(
            pd.crosstab(
                index=df_hts_selections['Month'],
                columns=df_hts_selections['HTSResult']
            ),
            markers=True,
            text='HTSResult', 
            title='HTS Trends'
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
                title='HTS_TST per Provider',
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
                title='Population HTS_TST per Provider',
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
        df_prevention_selections[df_prevention_selections['GBV'] != 'N/A']['First Name']))
    prepnewdf = df_prep[df_prep['Financial_Year'] == 'Vukisha_FY1']
    prepctdf = df_prep[df_prep['Status'] == 'Active']

    pnew = len(prepnewdf)
    pct = len(prepctdf)

    fsw = round(((kpfsw/KP_PREV_FSW)*100), 1)
    msm = round(((kpmsm/KP_PREV_MSM)*100), 1)
    p_GEND_GBV_KP = round(((kpGEND_GBV_KP/GEND_GBV_KP)*100), 1)
    ppnew = round(((pnew/PrEP_NEW_KP)*100),1)
    ppct = round(((pct/PrEP_CT_KP)*100),1)

    hed1, hed2, hed3, hed4, hed5 = st.columns(5)
    with st.container():
        with hed1:
            kpprevfsw = f"##### KP_PREV_FSW \n##### Target: {KP_PREV_FSW} \n##### Achievement: {kpfsw}({fsw})%"
            st.info(f"{kpprevfsw}")
        with hed2:
            kpprevmsm = f"##### KP_PREV_MSM \n##### Target: {KP_PREV_MSM} \n##### Achievement: {kpmsm}({msm}%)"
            st.info(f"{kpprevmsm}")
        with hed3:
            gendgbv = f"##### KP_GEND_GBV(KP) \n##### Target: {GEND_GBV_KP} \n##### Achievement: {kpGEND_GBV_KP}({p_GEND_GBV_KP}%)"
            st.info(f"{gendgbv}")
        with hed4:
            prepnew = f"##### PREP_NEW(KP) \n##### Target: {PrEP_NEW_KP} \n##### Achievement: {pnew}({ppnew}%) "
            st.info(f"{prepnew}")
        with hed5:
            prepct = f"##### PrEP_CT(KP) \n##### Target: {PrEP_CT_KP} \n##### Achievement: {pct}({ppct}%)"
            st.info(f"{prepct}")
    with st.container():
        st.plotly_chart(
            px.line(
                pd.crosstab(
                    columns=df_prevention_selections['KPType'],
                    index=df_prevention_selections['Month']
                ),
                markers=True,
                text='KPType',
                title='KP_PrEV Trends'
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
                    title='Monthly KP_PrEV Performance',
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
                    text='KPType',
                    title='Cummulative KP_PrEV Performance',
                ).update_traces(texttemplate="%{y}"),
                use_container_width=True
            )

        with col1:
            st.plotly_chart(
                px.histogram(
                    data_frame=df_prevention_selections[df_prevention_selections['GBV'] != 'N/A'],
                    x='Month',
                    color='GBV',
                    title='Monthly GEND_GBV Performance',
                    text_auto=True
                ), use_container_width=True
            )

        with col2:
            st.plotly_chart(
                px.line(
                    pd.crosstab(
                        columns=df_prevention_selections[df_prevention_selections['GBV']
                                                        != 'N/A']['GBV'],
                        index=df_prevention_selections[df_prevention_selections['GBV']
                                                    != 'N/A']['Month']
                    ).cumsum(),
                    title='Cummulative GEND_GBV(KP) Performance',
                    text='GBV'
                ).update_traces(texttemplate="%{y}"),
                use_container_width=True
            )
        with col1:
            st.plotly_chart(
                px.histogram(
                    data_frame=prepnewdf,
                    x='Month',
                    color='PopulationType',
                    category_orders={'Month': ['October', 'November', 'December',
                                            'January', 'February', 'March',
                                            'April', 'May', 'June',
                                            'July', 'August', 'September'],
                                            'PopulationType':['KeyPopulation','General Population']},
                    text_auto=True,
                    title='Monthtly PrEP_NEW Performance'
                ),use_container_width=True
            )
        with col2:
            st.plotly_chart(
                px.line(
                    pd.crosstab(
                        index=prepnewdf['Month'],
                        columns=prepnewdf['PopulationType']
                    ).cumsum(),
                    markers=True,
                    text='PopulationType',
                    title='Cummulative PrEP_NEW Performance'
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
                title='Provider Contribution to KP_PrEV',
                text_auto=True
            ), use_container_width=True
        )
    with col4:
        st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_month[df_prevention_month['GBV'] != 'N/A'],
                x='Provider',
                title='Provider GBV Case Identification',
                color='GBV',
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
        label="Download prevention data as CSV",
        data=csv,
        file_name='Prevention Linelist extract.csv',
        mime='text/csv',
    )
    st.dataframe(df_prevention_selections)
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df_prep)
    st.write('Prep Data')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='Prep Linelist extract.csv',
        mime='text/csv',
    )
    st.dataframe(df_prep)

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

    hed1, hed2, hed3, hed4 = st.columns(4)
    hed5,hed6, hed7,hed8 = st.columns(4)
    with st.container():

        with hed1:
            txcurr = f"##### TX_CURR(KP) \n##### Target: {TX_CURR_KP} \n##### Achievement: {curr}({currp}%)"
            st.info(f"{txcurr}")

        with hed2:
            txnew = f"##### TX_NEW(KP) \n##### Target: {TX_NEW_KP} \n##### Achievement: {new}({newp}%)"
            st.info(f"{txnew}")

        with hed3:
            cancer_ = f"##### CxCa(KP) \n##### Target: {CxCa_KP} \n##### Achievement: {cacx}({cacxp}%)"
            st.info(f"{cancer_}")
        with hed4:
            pvlsd = f"##### TX_PVLS_D(KP) \n##### Target: {TX_PVLS_D_KP} \n##### Achievement: 0 (0%)"
            st.info(f"{pvlsd}")
        with hed5:
            pvlsn = f"##### TX_PVLS_N(KP) \n##### Target: {TX_PVLS_N_KP} \n##### Achievement: 0 (0%)"
            st.info(f"{pvlsn}")
        with hed6:
            tbstat = f"##### TB_STAT(KP) \n##### Target: {TB_STAT_KP} \n##### Achievemnt: "
            st.info(f"{tbstat}")
        with hed7:
            tbprevd = f"##### TB_PREV_D(KP) \n##### Target: {TB_PREV_D_KP} \n##### Achievement: 0 (0%)"
            st.info(f"{tbprevd}")
        with hed8:
            tbprevn = f"##### TB_PREV_N(KP) \n##### Target: {TB_PREV_N_KP} \n##### Achievement: 0 (0%)"
            st.info(f"{tbprevn}") 
    
    st.plotly_chart(
        px.line(
            pd.crosstab(
                index=Fy['Month'],
                columns=Fy['PopulationType']
            ),
            markers=True,
            title='TX_NEW Trends',
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
                title='Monhtly TX_NEW  Performance',
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
                title='Monthly CxCa Performance',
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
                title='Cummulative TX_NEW  Performance',
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
                title='Cummulative CxCa Performance',
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
    #///////////////////////////////////////////////////////////////////////
    hed1, hed2, hed3, hed4, hed5, hed6 =st.columns(6)
    #HTS
    Financial_Year = st.sidebar.multiselect(
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
    KP = df_hts_selections[df_hts_selections['PopulationType']
                           == 'KeyPopulation']
    TST_Achievement_Neg = int(
        len(KP[KP['HTSResult'] == 'Negative']['First Name']))
    TST_Achievement_Pos = int(
        len(KP[KP['HTSResult'] == 'Positive']['First Name']))
    TST_Proportion = round(((TST_Achievement_Neg/HTS_TST_TARGET)*100), 1)
    Pos_Proportion = round(((TST_Achievement_Pos/HTS_TST_POS_TARGET)*100), 1)  
    #////////////////////////////////////////////////////////////////////////
    # Prevention
    Financial_Year = st.sidebar.multiselect(
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
    kppwid =  int(len(
        df_prevention_selections[df_prevention_selections['KPType'] == 'PWID']['First Name'])) 
    kptg = int(len(
        df_prevention_selections[df_prevention_selections['KPType'] == 'TG']['First Name'])) 
    kpGEND_GBV_KP = int(len(
        df_prevention_selections[df_prevention_selections['GBV'] != 'N/A']['First Name']))
    prepnewdf = df_prep[df_prep['Financial_Year'] == 'Vukisha_FY1']
    prepctdf = df_prep[df_prep['Status'] == 'Active']

    pnew = len(prepnewdf)
    pct = len(prepctdf)

    fsw = round(((kpfsw/KP_PREV_FSW)*100), 1)
    msm = round(((kpmsm/KP_PREV_MSM)*100), 1)
    
    p_GEND_GBV_KP = round(((kpGEND_GBV_KP/GEND_GBV_KP)*100), 1)
    ppnew = round(((pnew/PrEP_NEW_KP)*100),1)
    ppct = round(((pct/PrEP_CT_KP)*100),1)
    #//////////////////////////////////////////////////////////////////////////
    # Care & Treatment
    Status = st.sidebar.multiselect(
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
    #////////////////////////////////////////////////////////////////////////////    
    with st.container():
        with hed1:
            st.info(f"##### County SNU: \n##### Population Estimate: \n##### Coverage: ")
            tst = f"##### HTS_TST_NEG(KP) \n##### Target: {HTS_TST_TARGET} \n##### Achievement: {TST_Achievement_Neg}({TST_Proportion}%)"
            st.info(f"{tst}")
            cancer_ = f"##### CxCa(KP) \n##### Target: {CxCa_KP} \n##### Achievement: {cacx}({cacxp}%)"
            st.info(f"{cancer_}")
            tbprevd = f"##### TB_PREV_D(KP) \n##### Target: {TB_PREV_D_KP} \n##### Achievement: 0 (0%)"
            st.info(f"{tbprevd}")
        with hed2:
            kpprevfsw = f"##### KP_PREV_FSW \n##### Target: {KP_PREV_FSW} \n##### Achievement: {kpfsw}({fsw})%"
            st.info(f"{kpprevfsw}")
            pos = f"##### HTS_POS(KP) \n##### Target: {HTS_TST_POS_TARGET} \n##### Achievement: {TST_Achievement_Pos}({Pos_Proportion}%)"
            st.info(f"{pos}")
            txnew = f"##### TX_NEW(KP) \n##### Target: {TX_NEW_KP} \n##### Achievement: {new}({newp}%)"
            st.info(f"{txnew}")
            tbprevn = f"##### TB_PREV_N(KP) \n##### Target: {TB_PREV_N_KP} \n##### Achievement: 0 (0%)"
            st.info(f"{tbprevn}") 
        with hed3:
            kpprevmsm = f"##### KP_PREV_MSM \n##### Target: {KP_PREV_MSM} \n##### Achievement: {kpmsm}({msm}%)"
            st.info(f"{kpprevmsm}")  
            self = f"##### HTS_SELF(KP) \n##### Target: {HTS_SELF_KP} \n##### Achievement: "
            st.info(f"{self}")
            txcurr = f"##### TX_CURR(KP) \n##### Target: {TX_CURR_KP} \n##### Achievement: {curr}({currp}%)"
            st.info(f"{txcurr}")
            gendgbv = f"##### KP_GEND_GBV(KP) \n##### Target: {GEND_GBV_KP} \n##### Achievement: {kpGEND_GBV_KP}({p_GEND_GBV_KP}%)"
            st.info(f"{gendgbv}")
        with hed4:
            prepnew = f"##### PREP_NEW(KP) \n##### Target: {PrEP_NEW_KP} \n##### Achievement: {pnew}({ppnew}%) "
            st.info(f"{prepnew}")
            recent = f"##### HTS_RECENT(KP) \n##### Target: {HTS_RECENT_KP} \n##### Achievement: "
            st.info(f"{recent}")
            pvlsd = f"##### TX_PVLS_D(KP) \n##### Target: {TX_PVLS_D_KP} \n##### Achievement: 0 (0%)"
            st.info(f"{pvlsd}")
            pwid = f"##### KP_PrEV_PWID \n##### Target: N/A \n##### Achievement: {kppwid}"
            st.info(f"{pwid}")

        with hed5:
            prepct = f"##### PrEP_CT(KP) \n##### Target: {PrEP_CT_KP} \n##### Achievement: {pct}({ppct}%)"
            st.info(f"{prepct}")
            txcurr = f"##### TX_CURR(KP) \n##### Target: {TX_CURR_KP} \n##### Achievement: {curr}({currp}%)"
            st.info(f"{txcurr}")
            pvlsn = f"##### TX_PVLS_N(KP) \n##### Target: {TX_PVLS_N_KP} \n##### Achievement: 0 (0%)"
            st.info(f"{pvlsn}")
            tg = f"##### KP_PrEV_PWID \n##### Target: N/A \n##### Achievement: {kptg}"
            st.info(tg)
        with hed6:
            tst = f"##### HTS_TST_NEG(KP) \n##### Target: {HTS_TST_TARGET} \n##### Achievement: {TST_Achievement_Neg}({TST_Proportion}%)"
            st.info(f"{tst}")            
            txnew = f"##### TX_NEW(KP) \n##### Target: {TX_NEW_KP} \n##### Achievement: {new}({newp}%)"
            st.info(f"{txnew}")
            tbstat = f"##### TB_STAT(KP) \n##### Target: {TB_STAT_KP} \n##### Achievemnt: "
            st.info(f"{tbstat}")
    chat1, chat2, chat3 = st.columns(3)   
    with st.container():
        with chat1:
            st.plotly_chart(
                px.pie(
                    data_frame=df_overview,
                    names='Sub_County',
                    title='Sub County Proportion of Clients'
                ), use_container_width=True
            )       
        with chat2:
            st.plotly_chart(
                px.pie(
                    data_frame=df_overview,
                    names='Program',
                    title='Programs Proportion of Clients'
                ),use_container_width=True
            )
        with chat3:
            st.plotly_chart(
                px.histogram(
                    data_frame=df_overview,
                    x='Sub_County',
                    color='Program',
                    barmode='group',
                    text_auto=True,
                    title='Program Distribution Per Sub County',
                ),
                use_container_width=True
            )
    st.map()
# %%
page_names_to_funcs = {
    "Overview": Overview,
    "HIV Testing Services": page2,
    "Prevention Services": page3,
    "HIV Care & Treatment": page4
}

selected_page = st.radio("Select a page", page_names_to_funcs.keys())

page_names_to_funcs[selected_page]()