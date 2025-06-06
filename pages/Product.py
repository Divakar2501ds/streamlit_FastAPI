import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import streamlit as st
from config import config_url
import time 
from streamlit_autorefresh import st_autorefresh
st.set_page_config(layout="wide")
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
if not token:
    st.error("Session Expired")
    if st.button("Go back to login"):
        st.switch_page("pages/Login.py")
    st.stop()


headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{config_url}/protected", headers=headers)
if response.status_code != 200:
    st.error("Session expired. Please log in again.")
    st.error("Session Expired")
    if st.button("Go back to login"):
        st.switch_page("pages/Login.py")
    st.stop()

category_id = st.query_params.get("category_id", [None])[0]
user_id = st.session_state.get("user_id")


if not user_id:
    st.error("🚫 Please log in to continue.")
    if st.button("Go back to login"):
        st.switch_page("pages/Login.py")
    st.stop()

if category_id is None:
    category_id = st.session_state.get("category_id")

if category_id is None:
    st.warning("⚠️ No category selected - Login to continue.")
    if st.button("Login"):
        st.switch_page("pages/Login.py")
    st.stop()



col_left, col_spacer, col_right = st.columns([2, 6, 4])


with col_left:
    if st.button("⬅ Go Back to Category", use_container_width=True):
        st.switch_page("pages/category.py")

with col_right:
    col_add, col_update = st.columns([1, 1])
    with col_add:
        if st.button(" Add Product", use_container_width=True):
            st.switch_page("pages/add_products.py")


st.title(" Products")

try:
        headers = {"Authorization": f"Bearer {token}"}

    
        response = requests.get(f"{config_url}/products/category/{category_id}",headers=headers)
        response.raise_for_status()
        jsondata = response.json()
        products = jsondata["data"]

        cols_per_row = 3

        for i in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(products):
                    product = products[i + j]
                    product_id = product.get("product_id")
                    product_name = product.get("product_name")
                    price = product.get("price")

                    raw_img_path = product.get("image_url") 
                    image_url = f"http://127.0.0.1:8000{raw_img_path}" 

                    with cols[j]:
                        try:
                            img_response = requests.get(image_url)
                            img_response.raise_for_status()
                            img = Image.open(BytesIO(img_response.content)).convert("RGB")
                            img = img.resize((800, 600)) 
                            st.image(img, use_container_width=True)
                        except Exception as e:
                            st.warning(f"Image load failed: {e}")

                        st.subheader(product_name)
                        st.caption(f"💰 Price: ₹{price}")

                        if st.button("View Details", key=f"view_{product['product_id']}"):
                            st.session_state["product_id"] = product["product_id"]
                            st.query_params["product_id"] = product["product_id"]
                            st.switch_page("pages/Product_details.py")
                        if st.button("Update product", key =f"update_{product['product_id']}"):
                            st.session_state["product_id"] = product["product_id"]
                            st.query_params["product_id"] = product["product_id"]
                            st.switch_page("pages/update_product.py")

except requests.RequestException as e:
        st.error(f"Failed to fetch products: {e}")

