#
# page2_tables.py
#
# Streamlit code for the pytock project.
#

import streamlit as st
import exceptions
import validators
import restaurant


#
# Toasts
#
# It turns out you need this rigmarole to execute toasts properly with page
# reloads and caching. The toasts are accumulated in our session state, where
# they stay until we get a chance to execute on them.
#

if "page2_toast" in st.session_state:
    text = st.session_state["page2_toast"]
    st.session_state["page2_toast"] = False
    if text:
        st.toast(text, icon=":material/info:")

def toast(text: str) -> None:
    st.session_state["page2_toast"] = text


#
# Table management
#

st.markdown("### Tables")

# clearErrors
#
# This page stores errors in the session state so that we can keep them until
# the user makes some change to an input field. For the text-entry fields we
# need to wait until they click outside the field or type Enter in order to
# execute our code.
#
# Error management is also the reason for not using streamlit forms, because
# that would disallow callbacks for all but the submit button and make it
# impossible to clear the errors after user data entry.
#
def clearErrors():
    st.session_state["tables_errors"] = []

# tables & bookings
#
# Please see restaurant.py for more information about these classes. Instances
# are created on the fly each time our page runs.
#
tables = restaurant.Tables()
bookings = restaurant.Bookings()

# the following are input fields for taking, releasing, and deleating tables

st.selectbox("Table", tables.namelist(), key="man_tablename", on_change=clearErrors)

if len(tables.tables) == 0:                                 # handle case of user deleting all tables
    take_disable = True
    release_disable = True
    delete_disable = True
else:
    release_disable = bookings.walkInAvailable(st.session_state["man_tablename"])
    take_disable = not release_disable
    delete_disable = False

# process the action buttons

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Take the table", disabled=take_disable):
        try:
            toast("The Table is Taken")
            bookings.walkIn(st.session_state["man_tablename"])
        except exceptions.TableBusyError:
            st.warning("The table was already taken")

with col2:
    if st.button("Release the table", disabled=release_disable):
        try:
            toast("The Table is Released")
            bookings.walkOut(st.session_state["man_tablename"])
        except exceptions.TableFreeError:
            st.warning("The table was already released")

with col4:
    if st.button("Delete", disabled=delete_disable):
        toast("The Table is Deleted")
        tables.deleteTable(st.session_state["man_tablename"])

#
# input fields for adding tables
#
# Validation is performed by separate functions to avoid making the Booking(s)
# and Table(s) classes overly complex, but also to provide isolation between
# the UI and the "business logic" of the reservations. In theory the validator
# functions could be shared among many classes. The validators return a clean
# version of the text given to them, reporting errors only if necessary.
#
# Errors found by the validators are accumulated and presented to the user all
# at once, because requiring that they be fixed one at a time is often annoying.
#

table_name = st.text_input("Name of table to Add", value=tables.defName(), on_change=clearErrors)
table_seats = st.number_input("Number of seats", value=restaurant.Tables.DEF_SEATS, on_change=clearErrors)
added = st.button("Add")
if added:
    errors = []

    # name check
    error, text = validators.validate_tablename(table_name)
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

    if len(errors) == 0:                                    # we proceed on no errors
        try:
            toast("The Table has been Added")
            tables.createTable(table_name, table_seats)
        except Exception as error:
            errors.append("An internal error occurred")     # errors should be caught in validator

    # save and report any errors
    st.session_state["tables_errors"] = errors
    for error in errors:
        st.error(error)
