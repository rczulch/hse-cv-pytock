#
# page1_booking.py
#
# Streamlit code for the pytock project.
#

import streamlit as st
import exceptions
import validators
import restaurant


#
# Booking management
#

st.markdown("### Booking")

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
    st.session_state["advertised"] = True                   # clear advertisement
    st.session_state["booking_errors"] = []                 # clear errors

# tables & bookings
#
# Please see restaurant.py for more information about these classes. Instances
# are created on the fly each time our page runs.
#
tables = restaurant.Tables()
bookings = restaurant.Bookings()
status = bookings.tableStatus()
if len(status) > 0:
    st.session_state["advertised"] = True                   # clear advertisement on first remote booking

# advertise our real-time updating until first user input or remote booking seen

if not "advertised" in st.session_state:
    st.info( \
        """
        Pytock supports multiple-window real-time updates. Please open a second window to see this.
        """, icon="🔥")

# the following are input fields for adding a booking

book_name = st.text_input("Input name", key="book_name", on_change=clearErrors)
book_phone = st.text_input("Input phone", key="book_phone", placeholder="+7 (999) 999 99-99 -- or any number", on_change=clearErrors)
col_left, col_right = st.columns(2)

with col_left:
    deftime = restaurant.Booking.defBookingTime()
    book_from = st.time_input("From", key="book_from", value=deftime, step=900, on_change=clearErrors)

with col_right:
    defperiod = restaurant.Booking.defBookingPeriod()
    book_period = st.time_input("Period", key="book_period", value=defperiod, step=900, on_change=clearErrors)

book_tablename = st.selectbox("Select table", tables.namelist(), key="book_tablename", on_change=clearErrors)

#
# validate and make booking
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

if len(tables.tables) == 0:                                 # handle if user deleted all tables
    submit_disable = True
else:
    submit_disable = False

submitted = st.button("Submit", disabled=submit_disable)
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
        book_phone = text

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
    error, text = validators.validate_tablename(book_tablename)
    if error:
        errors.append(error)
    else:
        book_tablename = text

    if len(errors) == 0:                                    # we proceed on no errors
        booking = restaurant.Booking(book_tablename, book_name, book_phone, book_from, book_period)
        try:
            bookings.add(booking)
        except exceptions.TableBusyError:
            errors.append("Table not available during that time")
        except exceptions.DuplicateBookingError:
            errors.append("Customer is already booked during that time")

    # save and report any errors in UI
    st.session_state["booking_errors"] = errors
    for error in errors:
        st.error(error)

#
# Table status
#
# This organizes the status by first table, and then possibly multiple bookings
# for each table. In a real system one might prefer to show strictly in time
# order, however the assignment examples had table first so we use that here.
#

if len(tables.tables) == 0:
    st.markdown(f"No tables defined. Please add some on **Table Management** page.")
else:
    for table in tables.tables:
        col_table, col_state = st.columns([0.3, 0.7])
        with col_table:
            st.markdown(table.description())                # e.g. "Table 1 - 4 seats"
        with col_state:
            col_time, col_delete = st.columns([0.8, 0.2])
            if not table.name in status:
                with col_time:
                    st.markdown("*Free*")                   # "Free" in italics
            else:
                for booking in status[table.name]:
                    with col_time:
                        st.markdown(booking.description())  # time / period and name / phone
                    with col_delete:
                        # The following delete button uses a custom keyString
                        # because streamlit requires that all buttons have a
                        # unique identifier in the session state.
                        if st.button("Delete", key=booking.keyString()):
                            bookings.delete(booking)
