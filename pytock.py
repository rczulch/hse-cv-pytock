#
# pytock.py
#

import time
import streamlit as st
import pytock_data

#
# logo with size override to make larger
#

st.logo(
    "resources/PytockLogo.svg",
    size="large"
)

st.html("""
  <style>
    [alt=Logo] {
      height: 10rem;
    }
  </style>
        """)

#
# Create page content
#

page1_booking = st.Page("page1_booking.py", title="Booking")
page2_tables = st.Page("page2_tables.py", title = "Table Management")
page3_status = st.Page("page3_status.py", title = "Table Status")

#
# Sidebar navigation
#

pg = st.navigation([page1_booking, page2_tables, page3_status], position="sidebar")
pg.run()
