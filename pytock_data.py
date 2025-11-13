#
# pytock_data.py
#
# Data/state services for the pytock application.
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
def rerun_sessions():
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
# Get the specified shared data by key, or None if unset.
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
# Set the specified shared data by key and notify of changes.
#
def set(key, data):
    global pytockData
    getinit()
    if key not in pytockData or pytockData[key] != data:
        if isinstance(data, (list,dict)):
            data = data.copy()
        pytockData[key] = data
        rerun_sessions()
