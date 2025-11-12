#
# page1_booking.py
#

import streamlit as st
import pytock_data
import validators
import restaurant

st.markdown("### Booking")

def text_change():
    test_data = st.session_state["test_data"]
    print(f"text_change: {test_data}")
    pytock_data.set("test_data", test_data)

#
# Book a table
#

def clearErrors():
    st.session_state["submit_errors"] = []

book_name = st.text_input("Input name", key="book_name", on_change=clearErrors)
book_phone = st.text_input("Input phone", key="book_phone", placeholder="+7 (999) 999 99-99", on_change=clearErrors)
col_left, col_right = st.columns(2)

with col_left:
    deftime = restaurant.Booking.defBookingTime()
    book_from = st.time_input("From", key="book_from", value=deftime, step=900, on_change=clearErrors)

with col_right:
    defperiod = restaurant.Booking.defBookingPeriod()
    book_period = st.time_input("Period", key="book_period", value=defperiod, step=900, on_change=clearErrors)

book_table = st.selectbox("Select table", ("table 1", "table 2", "table 3"), key="book_table", on_change=clearErrors)
bookings = restaurant.Bookings()

submitted = st.button("Submit")
if submitted:
    errors = []

    # name check
    error, text = validators.validate_name(book_name)
    if error:
        errors.append(error)
    else:
        book_name = text
    
    # phone check
    error, text = validators.validate_phone(book_phone)
    if error:
        errors.append(error)
    else:
        book_name = text

    # timeOfDay check
    error, tod = validators.validate_timeOfDay(book_from)
    if error:
        errors.append(error)
    else:
        book_from = tod

    # period check
    error, time = validators.validate_timePeriod(book_period)
    if error:
        errors.append(error)
    else:
        book_period = time

    # table syntactical check
    error, text = validators.validate_table(book_table)
    if error:
        errors.append(error)
    else:
        book_table = text

    if len(errors) == 0:
        booking = restaurant.Booking(book_table, book_name, book_phone, book_from, book_period)
        try:
            bookings.add(booking)
        except Exception as error:
            errors.append(error)

    # save and report any errors
    st.session_state["submit_errors"] = errors
    for error in errors:
        st.error(error)

### display bookings here


#
# Table status page
#

tables = pytock_data.get("book_table")
if not tables:
    st.markdown("No tables defined. Please add some on **Table Management** page.")
else:
    for table in tables:
        col_table, col_state, col_delete = st.columns(3)

