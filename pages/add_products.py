import streamlit as st
import requests
import time
from config import config_url
from pages.token import check_token
from streamlit_autorefresh import st_autorefresh
hide_sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st_autorefresh(interval=60 * 1000, key="auth_check")
token =  st.session_state.get("access_token")
check_token()
headers = {"Authorization": f"Bearer {token}"}



col_left, col_spacer, col_right = st.columns([2, 6, 4])
with col_left:
    if st.button("⬅ Go Back to Category", use_container_width=True):
        st.switch_page("pages/category.py")
st.title("Add New Product")


try:
    response = requests.get(f"{config_url}/categories",headers=headers)
    response.raise_for_status()
    categories = response.json()
    category_options = {cat["category_name"]: cat["category_id"] for cat in categories}
except Exception as e:
    st.error(f"Could not load categories: {e}")
    st.stop()

product_name = st.text_input("Product Name")
product_description = st.text_area("Product Description")

price = st.number_input("Product Price", min_value=0.0, format="%.2f")

selected_category = st.selectbox("Select Category", list(category_options.keys()))

image_file = st.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"])
if st.button("Submit"):
    if all([product_name, product_description, price, selected_category, image_file]):
        try:
            files = {
                "file": (image_file.name, image_file, image_file.type)
            }
            data = {
                "product_name": product_name,
                "product_description": product_description,
                "price": str(price),  
                "category_id": str(category_options[selected_category])
            }
            res = requests.post(f"{config_url}/add_product", data=data, files=files, headers=headers)

            if res.status_code == 200:
                st.success("Product added successfully!")
                time.sleep(1)
                st.switch_page("pages/category.py")
            else:
                st.error(f"Failed to add product: {res.text}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill out all fields and upload an image.")
