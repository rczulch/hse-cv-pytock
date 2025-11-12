#
# page2_tables.py
#

import streamlit as st
import exceptions
import validators
import restaurant

st.markdown("### Tables")

#
# Manage tables
#

def clearErrors():
    st.session_state["tables_errors"] = []

tables = restaurant.Tables()
bookings = restaurant.Bookings()

man_tablename = st.selectbox("Table", tables.namelist(), key="man_tablename", on_change=clearErrors)
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Take the table"):
        try:
            st.toast("The Table is Taken")
            bookings.walkIn(man_tablename)
        except exceptions.TableBusyError:
            st.warning("The table was already taken")

with col2:
    if st.button("Release the table"):
        try:
            bookings.walkOut(man_tablename)
            st.info("The Table is Released")
        except exceptions.TableFreeError:
            st.warning("The table was already released")

with col4:
    if st.button("Delete"):
        tables.deleteTable(man_tablename)

table_name = st.text_input("Name of table to Add", value=tables.defName(), on_change=clearErrors)
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
