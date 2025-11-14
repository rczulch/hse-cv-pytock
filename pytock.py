#
# pytock.py
#
# Main streamlit file for the restaurant reservation project.
# HSE AI & CV Program
# Object Oriented Programming course
#
# submitted by Richard Zulch
#
# Usage: streamlit run pytock.py
#
# Note: "tock" is a popular restaurant management system in the US,
# so this is named "pytock" to follow pythonic naming conventions.
#

import streamlit as st

#
# Logo with size override in HTML to make larger
#

st.logo(
    "resources/PytockLogo.svg",
    size="large",
    link="https://www.exploretock.com"
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
