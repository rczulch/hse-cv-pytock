#
# page2_tables.py
#

import streamlit as st
import pytock_data
import validators
import restaurant

st.markdown("### Tables")

#
# Manage tables
#

def clearErrors():
    st.session_state["tables_errors"] = []

book_table = st.selectbox("Select table", ("table 1", "table 2", "table 3"), key="book_table", on_change=clearErrors)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button("Take the table")

with col2:
    st.button("Release the table")

with col4:
    st.button("Delete")

tables = restaurant.Tables()
table_name = st.text_input("Name of table", value=tables.defName(), on_change=clearErrors)
table_seats = st.number_input("Number of seats", value=restaurant.Tables.DEF_SEATS, on_change=clearErrors)
added = st.button("Add")
if added:
    errors = []

    # name check
    error, text = validators.validate_table(table_name)
    if error:
        errors.append(error)
    else:
        table_name = text

    # name check
    error, seats = validators.validate_seats(table_seats)
    if error:
        errors.append(error)
    else:
        table_seats = seats

    if len(errors) == 0:
        try:
            tables.createTable(table_name, table_seats)
        except Exception as error:
            errors.append(error)

    # save and report any errors
    st.session_state["tables_errors"] = errors
    for error in errors:
        st.error(error)
