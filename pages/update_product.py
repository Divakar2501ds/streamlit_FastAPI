import streamlit as st
import requests
from pages.token import check_token
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
check_token()
headers = {"Authorization": f"Bearer {token}"}



product_id = st.session_state.get("product_id", None)

if not product_id:
    st.error("No product selected. Please go back and choose a product.")
    if st.button("Go back to login"):
        st.switch_page("pages/Login.py")
    st.stop()
col_left, col_spacer, col_right = st.columns([2, 6, 4])


with col_left:
    if st.button("⬅ Go Back to Products", use_container_width=True):
        st.switch_page("pages/Product.py")
st.title("Update Product")

try:
    response = requests.get(f"http://127.0.0.1:8000/products/product/{product_id}",headers=headers)
    response.raise_for_status()
    product = response.json()
except Exception as e:
    st.error(f"Could not load products: {e}")
    st.stop()
product_name = st.text_input(f"Product ID {product_id}", value=product.get("product_name", ""))
product_name = st.text_input("Product Name")
product_description = st.text_area("Product Description")
price = st.number_input("Product Price", min_value=0.0, format="%.2f")
image_file = st.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"])

if st.button("Submit"):
    if not product_id:
        st.warning("Please enter a valid Product ID.")
    elif not all([product_name, product_description, price, image_file]):
        st.warning("Please fill out all fields and upload an image.")
    else:
        try:
            files = {
                "file": (image_file.name, image_file.getbuffer(), image_file.type)
            }
            data = {
                "product_name": product_name,
                "product_description": product_description,
                "price": str(price),
            }
            res = requests.patch(f"http://127.0.0.1:8000/update_product/{product_id}", data=data, files=files)

            if res.status_code == 200:
                st.success("Product updated successfully!")
            else:
                st.error(f"Failed to update product: {res.text}")
        except Exception as e:
            st.error(f"Error: {e}")
