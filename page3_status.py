#
# page3_status.py
#

import streamlit as st
import pytock_data
import validators
import restaurant

st.markdown("### Status")

#
# Table status
#

tables = pytock_data.get("book_table")
if not tables:
    st.markdown("No tables defined. Please add some on **Table Management** page.")
else:
    for table in tables:
        col_table, col_state, col_delete = st.columns(3)

