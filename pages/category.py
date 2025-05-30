import streamlit as st
import requests
from config import config_url
import time
from PIL import Image
from io import BytesIO
import os

st.set_page_config(layout="wide")
hide_sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)


user_id = st.session_state.get("user_id")
if not user_id:
    st.error("🚫 Please log in to continue.")
    if st.button("Go back to login"):
        st.switch_page("pages/Login.py")
    st.stop()

st.session_state["user_id"] = user_id
st.query_params["user_id"] = user_id

if st.button("Add Category", key="add_cat_btn"):
    st.switch_page("pages/add_category.py")
st.title(" Categories")

try:
    response = requests.get(f"{config_url}/categories")
    response.raise_for_status()
    categories = response.json()
    cols = st.columns(3)
    for idx, cat in enumerate(categories):
        col = cols[idx % 3]
        cat_id = cat.get("category_id")
        cat_name = cat.get("category_name")
        is_deleted = cat.get("is_deleted")
        raw_path = cat.get("image_url")  
        st.session_state["category_id"] = cat.get("category_id")
        category_id = st.session_state["category_id"]
        image_url = f"{config_url}{raw_path}" 

        with col:
            try:
                img_response = requests.get(image_url)
                img_response.raise_for_status()
                img = Image.open(BytesIO(img_response.content))
                img = img.resize((400, 300))
                st.image(img, use_container_width = True)
            except Exception as e:
                st.warning(f"Image not found or failed to load: {e}")

            st.markdown(f"### {cat_name}")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("View Products", key=f"view_{cat_id}"):
                    st.session_state["category_id"] = cat_id
                    st.query_params["category_id"]=cat_id
                    st.switch_page("pages/Product.py")
            with col2:
                if st.button("Delete Category",key=f"delete_category_btn{cat_id}"):
                    response1 = requests.delete(f"{config_url}/delete_category/{category_id}")
                    if response1.status_code == 200:
                        st.success("Deleted category successfully")
                    else:
                        st.error("The category is in the cart ,it cannot be deleted ")
                        time.sleep(2)
                        st.rerun()
            with col3:
                if st.button("update category",key=f"update_category_btn{cat_id}"):
                        st.session_state["category_id"] = cat_id
                        st.session_state["category_name"] = cat_name
                        st.switch_page("pages/update_category.py")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching categories: {e}")

