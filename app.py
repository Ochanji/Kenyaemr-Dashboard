import streamlit as st

import ct, hts, overview, prevention  # import your app modules here
from multiapp import MultiApp

st.set_page_config(layout='wide',
                   page_title='Performance Dashboard',
                   page_icon=':bar_chart:',
                   initial_sidebar_state='collapsed'
                   )
app = MultiApp()
# Add all your application here
app.add_app("Overview", overview.app)
app.add_app("HTS Services", hts.app)
app.add_app("Prevention", prevention.app)
app.add_app("Care & Treatment", ct.app)
# app.add_app("Reporting", reporting.app)
# The main app
app.run()
