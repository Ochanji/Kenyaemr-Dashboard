import pandas as pd
import streamlit as st
import plotly.express as px

from dataset import df_ct

df_ct['Month'] = pd.Categorical(
    values=df_ct['Month'],
    categories=['October', 'November', 'December',
                'January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'August', 'September']
)
df_ct['Last Visit Month'] = pd.Categorical(
    values=df_ct['Last Visit Month'],
    categories=['October', 'November', 'December',
                'January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'August', 'September']
)


def app():
    st.markdown(
        '#### :bar_chart: Care & Treatment Dashboard'
    )

    Status = st.multiselect(
        'Select Care & Treament Status',
        options=df_ct['Status'].unique(),
        default=['On ART']
    )

    df_ct_selections = df_ct.query(
        "Status == @Status")

    Fy = df_ct_selections[df_ct_selections['Financial_Year_'] == 'Vukisha_FY1']
    Fyc = df_ct_selections[df_ct_selections['Financial_Year'] == 'Vukisha_FY1']

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
                data_frame=Fyc[Fyc['Gender'] == 'F'],
                x='Last Visit Month',
                color='CaCx',
                barmode='group',
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
                    index=Fyc[Fyc['Gender'] == 'F']['Last Visit Month'],
                    columns=Fyc[Fyc['Gender'] == 'F']['CaCx']
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
