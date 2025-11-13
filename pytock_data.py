#
# pytock_data.py
#
# Data/state services for the pytock application. This module arranges for state
# to be cached and changes updated in all client browsers and tabs connected to
# this streamlit application.
#

import streamlit as st
from streamlit.runtime import Runtime
from streamlit.runtime.app_session import AppSession

# rerun_sessions
#
# Change notification to other tabs/browsers.  These functions identify the 
# browser sessions connected to our unified backend and cause them to rerun
# and thus update.
#
def rerun_sessions() -> None:
    def get_streamlit_sessions() -> list[AppSession]:
        runtime: Runtime = Runtime.instance()
        return [s.session for s in runtime._session_mgr.list_sessions()]

    for session in get_streamlit_sessions():
       session._handle_rerun_script_request(session._client_state)

# pytockData
#
# Our shared data state.
#
pytockData = { }

# getinit
#
# Return our shared data state under the cache_resource decorator, which makes
# it shared among all sessions/browsers that are accessing this page.
#
@st.cache_resource
def getinit():
    global pytockData
    return pytockData

# get
#
# Get the specified shared data by key, or None if unset. This copies the data
# in order to detect changes.
#
def get(key):
    global pytockData
    getinit()
    if key in pytockData:
        data = pytockData[key]
        if isinstance(data, (list,dict)):
            data = data.copy()
        return data
    return None

# set
#
# Set the specified shared data by key and notify of changes. This copies the
# data in order to detect changes. This makes the assumption that the changes we
# want to detect are in the top-level container being stored, so it only does a
# shallow copy. This way the streamlit cache resource here has its own container
# and can detect changes such as added or deleted bookings and tables. Were we
# to allow mutating table and booking objects then this would need a deep copy.
#
def set(key, data):
    global pytockData
    getinit()
    if key not in pytockData or pytockData[key] != data:
        if isinstance(data, (list,dict)):
            data = data.copy()
        pytockData[key] = data
        rerun_sessions()
