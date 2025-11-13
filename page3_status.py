#
# page3_status.py
#
# Streamlit code for the pytock project.
#

import streamlit as st
import restaurant


#
# Table status
#

st.markdown("### Status")

# tables & bookings
#
# Please see restaurant.py for more information about these classes. Instances
# are created on the fly each time our page runs.
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

#
# Table status
#
# This organizes the status by first table, and then possibly multiple bookings
# for each table. In a real system one might prefer to show strictly in time
# order, however the assignment examples had table first so we use that here.
#

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
