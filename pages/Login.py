import streamlit as st
import requests
import time
from config import config_url
hide_sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)


email = st.text_input("**📧 Enter your email**")
password = st.text_input(" **🔐 Enter a password**", type = "password")
col1, col2, col3 = st.columns(3)
with col2:

    if st.button("Login"):
        try:
            response = requests.post(
                f"{config_url}/login",
                json={"email": email, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state["user_id"] = data.get("user_id")
                st.session_state["access_token"]= data.get("access_token")
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                response1  = requests.get(f"{config_url}/protected",headers=headers)
                if  response1.status_code != 200:
                    st.error("failed to protect_route")
                    st.session_state.clear()
                    st.stop()

                if st.session_state.get("user_id"):
                    st.success("Logged in successfully!")
                    st.write("Your JWT token:")
                    st.code(data["access_token"])

                    time.sleep(3)
                    st.switch_page("pages/category.py")
                else:
                    st.error("Login failed: No user ID returned")
            else:
                st.write("Enter a registered email and password")
        except Exception as e:
            st.error(f"Error: {e}")


