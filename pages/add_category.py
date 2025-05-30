import streamlit as st
import requests
from config import config_url
st.set_page_config(layout="wide")
hide_sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)



col_left, col_spacer, col_right = st.columns([2, 6, 4])


with col_left:
    if st.button("⬅ Go Back to Category", use_container_width=True):
        st.switch_page("pages/category.py")

st.title(" Add New Category")

category_name = st.text_input("Category Name")
image_file = st.file_uploader("Upload Category Image", type=["png", "jpg", "jpeg"])

if st.button("Submit"):
    if category_name and image_file:
        files = {
            "file": (image_file.name, image_file, image_file.type)
        }
        data = {
            "category_name": category_name
        }
        try:
            res = requests.post(f"{config_url}/add_category", data=data, files=files)
            if res.status_code == 200:
                st.success("Category added successfully!")
            else:
                st.error(res.json())
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please provide both name and image.")
