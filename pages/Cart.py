import streamlit as st
import requests
from PIL import Image
from io import BytesIO
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

user_id = st.session_state.get("user_id")
if not user_id:
    st.error("You must be logged in to view your cart.")
    if st.button("Login"):
        st.switch_page("pages/Login.py")

    st.stop()
col_left, col_spacer, col_right = st.columns([2, 6, 4])


with col_left:
    if st.button("⬅ Go Back to Category", use_container_width=True):
        st.switch_page("pages/category.py")

query_params = st.query_params
product_id = query_params.get("product_id", [None])[0]
category_id = query_params.get("category_id", [None])[0]
st.title(" Your Cart")

try:
    response = requests.get(f"{config_url}/cart", params={"user_id": user_id})
    response.raise_for_status()
    cart_items = response.json()
    if not cart_items:
        st.info("Your cart is empty.")
    else:
        total_cost = 0
        for idx, item in enumerate(cart_items):
            product_id = item.get("product_id")
            category_id = item.get("category_id")  # if needed

            with st.container():
                cols = st.columns([1, 3, 1, 1, 1])
                with cols[0]:
                    raw_img_path = item.get("image_url")
                    image_url = f"{config_url}{raw_img_path}"

                    try:
                        img_response = requests.get(image_url)
                        img_response.raise_for_status()
                        img = Image.open(BytesIO(img_response.content)).convert("RGB")
                        st.image(img, width=250)
                    except Exception as e:
                        st.warning(f"Image load failed: {e}")

                with cols[1]:
                    st.subheader(item["product_name"])
                with cols[2]:
                    st.write(f"₹{item['price_per_unit']}")
                with cols[3]:
                    qty_input = st.number_input(
                        label="Qty", min_value=1, max_value=100, value=item['quantity'], step=1, key=f"qty_{product_id}_{idx}"
                    )
                with cols[4]:
                    st.write(f"Total: ₹{item['price_at_time']}")
                    total_cost += item["price_at_time"]

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(" Delete", key=f"delete_{product_id}_{idx}"):
                        try:
                            del_response = requests.delete(f"{config_url}/delete_item", params={
                                "user_id": user_id,
                                "product_id": product_id,
                                "category_id": category_id

                            })
                            if del_response.status_code == 200:
                                st.success("Item deleted!")
                                st.rerun()
                            else:
                                st.error("Failed to delete item.")
                        except Exception as e:
                            st.error(f"Error: {e}")

                with col2:
                    if st.button("Update Qty", key=f"update_{product_id}_{idx}"):
                        try:
                            patch_response = requests.patch(f"{config_url}/cart/update_quantity", params={
                                "user_id": user_id,
                                "product_id": product_id,
                                "quantity": qty_input,
                                "category_id": category_id 
                            })
                            if patch_response.status_code == 200:
                                st.success("Quantity updated!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to update quantity.")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    st.markdown("<br><br>", unsafe_allow_html=True)

except Exception as e:
        st.error(f"Error: {e}")

