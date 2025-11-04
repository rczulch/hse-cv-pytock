#
# page1_booking.py
#

import streamlit as st
import pytock_data

st.write("Page 1 - booking")

def text_change():
    test_data = st.session_state["test_data"]
    print(f"text_change: {test_data}")
    pytock_data.set("test_data", test_data)

test_data = st.text_input("Please enter test data", key="test_data", on_change=text_change)
st.write("test data:", test_data)
