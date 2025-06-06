
import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh
from config import config_url
import time
def check_token():
    token =  st.session_state.get("access_token")
    if not token:
        st_autorefresh(interval=60000, key="auth_refresh")
        st.error("session expired")
        if st.button("Go back to login"):
            st.switch_page("pages/Login.py")
        st.stop()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{config_url}/protected",headers=headers)
    if response.status_code != 200:
        st.error("session expired")
        if st.button("Go back to login"):
            st.switch_page("pages/Login.py")
        st.stop()