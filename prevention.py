# %%
from pyparsing import col
from dataset import df_prevention
import streamlit as st
import plotly.express as px
import pandas as pd

df_prevention['Month'] = pd.Categorical(
    values=df_prevention['Month'],
    categories=['October', 'November', 'December', 
                'January','February','March',
                'April','May','June',
                'July','August','September']
)

# %%
def app():
    st.markdown('#### :bar_chart: Prevention Dashboard')
    Financial_Year = st.multiselect(
        'Financial Year',
        options=df_prevention['Financial_Year'].unique(),
        default=df_prevention['Financial_Year'].iloc[-1]
    )

    df_prevention_selections = df_prevention.query(
        "Financial_Year == @Financial_Year")
    
    kpfsw = int(len(df_prevention_selections[df_prevention_selections['KPType'] == 'FSW']['First Name']))
    kpmsm = int(len(df_prevention_selections[df_prevention_selections['KPType'] == 'MSM']['First Name']))
    kpgbv = int(len(df_prevention_selections[df_prevention_selections['GBV'] != 'N/A']['First Name']))
    
    KPPrev_fsw = 4152
    KPPrev_msm = 2400
    gbv = 1405 

    fsw = round(((kpfsw/KPPrev_fsw)*100),1)
    msm = round(((kpmsm/KPPrev_msm)*100),1)
    p_gbv = round(((kpgbv/gbv)*100),1)

    
    hed1, hed2 =st.columns(2)
    with hed1:
        st.markdown(f"###### KP_PREV_FSW Target: {KPPrev_fsw}")
        st.markdown(f"###### KP_PREV_FSW Target: {KPPrev_msm}")
        st.markdown(f"###### KP_GBV Target: {gbv}")
    with hed2:
        st.markdown(f"###### KP_PREV_FSW Achievement: {kpfsw} ({fsw}%)")
        st.markdown(f"###### KP_PREV_MSM Achievement: {kpmsm} ({msm}%)")
        st.markdown(f"###### KP_GBV Achievement: {kpgbv} ({p_gbv}%)")

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
    col1, col2 =st.columns(2)
    with col1:
        st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_selections,
                x='Month',
                color='KPType',
                text_auto=True,
                category_orders={'Month':['October', 'November', 'December', 
                                        'January','February','March',
                                        'April','May','June',
                                        'July','August','September'],
                                 'KPType':['FSW','MSM','PWID','TG']}
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
                data_frame=df_prevention_selections[df_prevention_selections['GBV'] != 'N/A'],
                x='Month',
                color='GBV',
                text_auto=True
            ),use_container_width=True
        )
    
    with col2:
        st.plotly_chart(
            px.line(
                pd.crosstab(
                    columns=df_prevention_selections[df_prevention_selections['GBV'] != 'N/A']['GBV'],
                    index=df_prevention_selections[df_prevention_selections['GBV'] != 'N/A']['Month']
                ).cumsum(),
                text='GBV'
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
            ),use_container_width=True
        )
    with col4:
        st.plotly_chart(
            px.histogram(
                data_frame=df_prevention_month[df_prevention_month['GBV'] != 'N/A'],
                x='Provider',
                color='GBV',
                text_auto=True
            ),use_container_width=True
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

