#
# page3_status.py
#

import streamlit as st
import restaurant

st.markdown("### Status")

#
# Table status
#

tables = restaurant.Tables()
bookings = restaurant.Bookings()

totalTables, totalSeats = tables.capacity()
usedTables, usedSeats = bookings.utilization()
st.markdown("""
            Tables: **{0}** free of **{1}** capacity  
            Seats: &nbsp; **{2}** free of **{3}** capacity  

            -----
            """.format(totalTables-usedTables, totalTables, totalSeats-usedSeats, totalSeats))

if len(tables.tables) != 0:
    status = bookings.tableStatus()
    for table in tables.tables:
        col_table, col_state = st.columns(2)
        with col_table:
            st.markdown(table.description())
        with col_state:
            if not table.name in status:
                st.markdown("*Free*")
            else:
                for booking in status[table.name]:
                    st.markdown(booking.description())
