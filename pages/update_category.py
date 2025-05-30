import streamlit as st
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

if "category_id" not in st.session_state:
    st.error("No category selected. Go back to the category page.")
    if st.button("Go Back to Categories"):
        st.switch_page("pages/category.py")
    st.stop()
col_left, col_spacer, col_right = st.columns([2, 6, 4])


with col_left:
    if st.button("⬅ Go Back to Category", use_container_width=True):
        st.switch_page("pages/category.py")
category_id = st.session_state["category_id"]
current_name = st.session_state.get("category_name", "")

st.title(f"Update Category: {current_name}")

new_name = st.text_input("New Category Name")
new_image = st.file_uploader("New Category Image", type=["jpg", "jpeg", "png", "webp"])
if st.button("Update Category", key=f"update_category_btn_{category_id}"):
        if not new_name or not new_image:
            st.warning("Please provide both a new name and a new image.")
        else:
            files = {
                "file": (new_image.name, new_image.getbuffer(), new_image.type)
            }
            data = {
                "category_name": new_name
            }

            response = requests.patch(
                f"{config_url}/categories/{category_id}",
                data=data,
                files=files
            )

            if response.status_code == 200:
                st.success("Category updated successfully!")
            else:
                st.error(f"Update failed: {response.status_code} - {response.text}")
