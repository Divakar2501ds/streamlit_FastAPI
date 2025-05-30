# import streamlit as st
# import requests
# col_left, col_spacer, col_right = st.columns([2, 6, 4])


# with col_left:
#     if st.button("⬅ Go Back to Category", use_container_width=True):
#         st.switch_page("pages/category.py")
# st.title("Update Product")

# try:
#     response = requests.get("http://127.0.0.1:8000/categories")
#     response.raise_for_status()
#     categories = response.json()
#     category_options = {cat["category_name"]: cat["category_id"] for cat in categories}
# except Exception as e:
#     st.error(f"Could not load categories: {e}")
#     st.stop()

# product_id = st.number_input("Product ID", min_value=1, step=1)
# product_name = st.text_input("Product Name")
# product_description = st.text_area("Product Description")
# price = st.number_input("Product Price", min_value=0.0, format="%.2f")
# selected_category = st.selectbox("Select Category", list(category_options.keys()))
# image_file = st.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"])

# if st.button("Submit"):
#     if not product_id:
#         st.warning("Please enter a valid Product ID.")
#     elif not all([product_name, product_description, price, selected_category, image_file]):
#         st.warning("Please fill out all fields and upload an image.")
#     else:
#         try:
#             files = {
#                 "file": (image_file.name, image_file.getbuffer(), image_file.type)
#             }
#             data = {
#                 "product_name": product_name,
#                 "product_description": product_description,
#                 "price": str(price),
#                 "category_id": str(category_options[selected_category])
#             }
#             res = requests.put(f"http://127.0.0.1:8000/update_product/{product_id}", data=data, files=files)

#             if res.status_code == 200:
#                 st.success("Product updated successfully!")
#             else:
#                 st.error(f"Failed to update product: {res.text}")
#         except Exception as e:
#             st.error(f"Error: {e}")
