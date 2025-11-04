#
# pytock.py
#

import time
import streamlit as st
import pytock_data

page1_booking = st.Page("page1_booking.py", title="Booking")
page2_tables = st.Page("page2_tables.py", title = "Table Management")
page3_status = st.Page("page3_status.py", title = "Table Status")

test_data = pytock_data.get("test_data") or ""
text_container = st.empty()
print(f"test_data displayed: {test_data}")
text_container.text(f"test_data: {test_data}")

pg = st.navigation([page1_booking, page2_tables, page3_status], position="sidebar")
pg.run()
