import streamlit as st
import requests
from PIL import Image
import time
from io import BytesIO
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

query_params = st.query_params
product_id = query_params.get("product_id", [None])[0]
category_id = query_params.get("category_id", [None])[0]

if category_id is None:
    category_id = st.session_state.get("category_id")
if product_id is None:
    product_id = st.session_state.get("product_id")

if category_id is None:
    st.error("please login to view your products")
    if st.button("Login"):
        st.switch_page("pages/Login.py")
    st.stop()

if product_id is None:
    st.error(" No product selected. Please go back and select a product.")
    st.stop()


st.session_state["category_id"] = category_id
st.session_state["product_id"] = product_id
st.query_params["product_id"] = product_id


col_left, col_spacer, col_right = st.columns([2, 6, 4])


with col_left:
    if st.button("⬅ Go Back to Products", use_container_width=True):
        st.switch_page("pages/Product.py")

product_id = st.session_state.get("product_id")
user_id = st.session_state.get("user_id")



if user_id is None:
    st.error("Go back to login")
    if st.button("Login"):
        st.switch_page("pages/Login.py")


response =  requests.get(f"{config_url}/products/product/{product_id}")
if response.status_code == 200:
    product = response.json()
    
    raw_img_path = product.get("image_url")

    image_url = f"{config_url}{raw_img_path}"

    try:
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        img = Image.open(BytesIO(img_response.content)).convert("RGB")
        st.image(img, width=250)
    except Exception as e:
        st.warning(f"Image load failed: {e}")
    st.subheader(product.get("product_name"))
    st.caption(product.get("product_description"))
    st.write(f"💰 Price: ₹{product.get('price')}")
    st.subheader("Select Quantity")
    qty = st.number_input("Quantity", min_value=1, max_value=100, value=1, step=1)
    quantity = qty  
    
    if st.button("Add to Cart"):
        if user_id and product_id and qty:
            params = {
                "user_id": user_id,
                "category_id": category_id,

            "product_id": product_id,
            "quantity": qty,
        }

            try:
                response1 = requests.post(f"{config_url}/add_to_cart", params=params)

                if response1.status_code == 200:
                    data = response1.json()
                    
                    if st.success(f"Added to cart! Total price: ₹{data.get('price_at_time')}"):
                        time.sleep(1)
                        st.switch_page("pages/Cart.py")
                elif response1.status_code == 409:
                    st.error("Item already there in your cart")
                else:
                    st.error(f"Failed: {response1.text}")
            except Exception as e:
               st.error(f"Error: {e}")
else:
    if st.button("Go to category page"):
        st.switch_page("pages/category.py")


