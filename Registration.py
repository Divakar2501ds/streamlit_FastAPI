import streamlit as st
import re
import time
import requests
from config import config_url
hide_sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""

st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.header("👤 Register your Account ")
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #008CBA;  
        color: white;              
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-size: 16px;
    }

    div.stButton > button:hover {
        background-color: #005f73;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("at least 8 characters long")
    if not any(c.islower() for c in password):
        errors.append("a lowercase letter")
    if not any(c.isupper() for c in password):
        errors.append("an uppercase letter")
    if not any(c.isdigit() for c in password):
        errors.append("a number")
    if not any(c in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for c in password):
        errors.append("a special character")

    if errors:
        return "Password must contain " + ", ".join(errors) + "."
    return None

role = st.selectbox("🎭 Role", ["user", "admin"])
email = st.text_input("📧 Enter your email")
password = st.text_input("🔐 Enter a password", type="password")

if st.button("🚀 Submit"):
    if not (email and password):
        st.error("Please fill all the details.")
    elif not is_valid_email(email):
        st.error("Invalid email format. Please enter a valid email.")
    else:
        pw_error = validate_password(password)
        if pw_error:
            st.error(pw_error)
        else:
  
            det = {
                "role": role,
                "email": email,
                "password": password
            }
            try:
                response = requests.post(f"{config_url}/register", json=det)
                if response.status_code == 200:
                    st.success(f"🎉 Registered as {role} successfully")
                    time.sleep(1)
                    st.switch_page("pages/Login.py") 
                else:
                    error_detail = response.json().get("detail", "An error occurred.")
                    st.error(error_detail)
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
if st.button(" **Already have an account - Sign in** "):
    st.switch_page("pages/Login.py")