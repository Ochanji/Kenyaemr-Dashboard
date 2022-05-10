# %%
from dataset import df_prevention, df_prevention_
import streamlit as st
import plotly.express as px
import pandas as pd

# %%
def app():
    st.markdown(':bar_chart: Prevention Dashboard')
    Financial_Year = st.multiselect(
        'Financial Year',
        options=df_prevention['Financial_Year'].unique(),
        default=df_prevention['Financial_Year'].iloc[-1]
    )

    df_prevention_selections = df_prevention.query(
        "Financial_Year == @Financial_Year")
    df_gbv = df_prevention_selections[df_prevention_selections['GBV'] != 'N/A']
    df_fsw = df_prevention_selections[df_prevention_selections['KPType'] == 'FSW']
    df_msm = df_prevention_selections[df_prevention_selections['KPType'] == 'MSM']
    df_prep = df_prevention_[df_prevention_['Financial_Year'] == 'Vukisha_FY1']
    df_prep_kp =df_prep[df_prep['PopulationType'] != 'General Population']
    df_prep_ =df_prevention_[df_prevention_['Month'] == 'April']
    FSW_target = 4152
    MSM_target = 2400
    Pnew_Target = 1006
    Pct_Target = 1409
    GBV_kp = 1405


    gbv = round(((len(df_gbv['First Name'])/GBV_kp)*100),1)
    fsw = round(((len(df_fsw['First Name'])/FSW_target)*100),1)
    msm = round(((len(df_msm['First Name'])/MSM_target)*100),1)
    pNew = round(((len(df_prep_kp['First Name'])/Pnew_Target)*100),1)
    

    # df_prevention_selections['Month'] = pd.Categorical(
    #     categories={'Month': ['October', 'November', 'December', 'January', 'February', 'March',
    #                                        'April', 'May', 'June', 'July', 'August', 'September']}
    # )

    header1, header2 = st.columns(2)
    with header1:
        st.markdown(f'####       KP_PrEV_FSW {fsw}%')
        st.markdown(f'####       KP_PrEV_MSM {msm}%')
        st.markdown(f'####       PrEP_NEW (KP) {pNew}%')
        st.markdown(f'####       GEND_GBV (KP)  {gbv}%')
    st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_selections,
                x='Month',
                barmode='group',
                color='KPType',
                text_auto=True,
                title='Monthly KP_PrEV Monthly Performance',
                category_orders={'Month': ['October', 'November', 'December', 'January', 'February', 'March',
                                           'April', 'May', 'June', 'July', 'August', 'September']}
            )#.update_traces(textposition='inside', textfont_size=14)
            ,
            use_container_width=True
        )
    st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_selections,
                x='Month',
                barmode='group',
                color='KPType',
                title='Cummultive KP_PrEV Performance',
                cumulative=True,
                text_auto=True,
                category_orders={'Month': ['October', 'November', 'December', 'January', 'February', 'March',
                                           'April', 'May', 'June', 'July', 'August', 'September']}
            )#.add_hline(y=4152, line_width=3, line_dash="dash", line_color="green").add_hline(y=2400, line_width=3, line_dash="dash", line_color="blue")
            ,
            use_container_width=True
        )   
    st.plotly_chart(
        px.histogram(
            data_frame=df_prevention_selections[df_prevention_selections['GBV'] != 'N/A'],
            title='Monthly GEND_GBV (KP)',
            x='Month',
            color='GBV',
            text_auto=True,
            barmode='group'
        ),
        use_container_width=True
    )
    st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_selections[df_prevention_selections['GBV'] != 'N/A'],
                title='Cumulative GEND_GBV (KP)',
                x='Month',
                color='GBV',
                text_auto=True,
                cumulative=True,
                barmode='group'
            ),
            use_container_width=True
        )
    st.plotly_chart(
        px.histogram(
            data_frame= df_prep,
            title='Monthly PrEP_NEW (KP) Performance',
            x='Month',
            color='PopulationType',
            text_auto=True,
        #    color='PopulationType',
            category_orders={'Month': ['October', 'November', 'December', 'January', 'February', 'March',
                                        'April', 'May', 'June', 'July', 'August', 'September']}
        ),
        use_container_width= True
    )
    st.plotly_chart(
            px.histogram(
               data_frame= df_prep,
               title='Cumulativative PrEP_NEW (KP) Performance',
               x='Month',
               color='PopulationType',
               text_auto=True,
               cumulative=True,
            #    color='PopulationType',
               category_orders={'Month': ['October', 'November', 'December', 'January', 'February', 'March',
                                           'April', 'May', 'June', 'July', 'August', 'September']}
            ),
            use_container_width=True
        )



    with header2:
        fsw_ = len(df_fsw['First Name'])
        msm_ = len(df_msm['First Name'])
        pNew_ = len(df_prep_kp['First Name'])
        gbv_ = len(df_gbv['First Name'])
        st.markdown(f'#### KP_PrEV_FSW Target: {FSW_target}, Achievement:{fsw_}')
        st.markdown(f'#### KP_PrEV_MSM Target: {MSM_target}, Achievement:{msm_}')
        st.markdown(f'#### PrEP_NEW (KP) Target: {Pnew_Target}, Achievement:{pNew_}')
        st.markdown(f'#### GEND_GBV (KP) Target: {GBV_kp}, Achievement: {gbv_} ')

        
        
    st.markdown('----')
    st.markdown('Monthly Performance Dashboards')
    st.markdown('----')
    Month = st.multiselect(
        'Month',
        options=df_prevention_selections['Month'].unique(),
        default=df_prevention_selections['Month'].iloc[-1]
    )

    df_prevention_month = df_prevention_selections.query(
        "Month == @Month")
    
    st.plotly_chart(
        px.line(
            pd.crosstab(
                index=df_prevention_month['Date'],
                columns=df_prevention_month['HIV Test']
            ),
            title='Daily trends',
            markers=True
        ).update_traces(textposition="bottom right"), 
        use_container_width=True
    )

    header3, header4 = st.columns(2)
    with header3:
        st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_month,#.fillna(0),
                title='Current monthly Provider Contribution to KP_PrEV',
                x='Provider',
                color='Type_Of_Visit',
                text_auto=True,
            )
        )
        st.plotly_chart(
            px.pie(
                title='PrEP CT'
            ),
            use_container_width=True
        )
    with header4:

        st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_month[df_prevention_month['GBV'] != 'N/A'],
                title='Current Month Provider GBV case Identification',
                x='Provider',
                color='GBV',
                text_auto=True
            ),
            use_container_width=True
        )
        st.plotly_chart(
            px.histogram(
                title='Current Month Provider PrEP Initiation',
                data_frame=df_prep_,
                x='Provider',
                color='PopulationType',
                text_auto=True
            ),
            use_container_width=True
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

    csv = convert_df(df_prep)
    st.write('Prep Data')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='PrepNew Linelist extract.csv',
        mime='text/csv',
    )
    st.dataframe(df_prep)

