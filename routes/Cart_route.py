
from fastapi import FastAPI, UploadFile, File, Form, Depends ,APIRouter ,HTTPException ,Query
from sqlalchemy.orm import Session
import shutil
from PIL import Image , ImageOps
import os
from typing import List 
from database import database
from database.database import get_db
from database.models import Cart, User, Product ,Category

router = APIRouter()

@router.post("/add_to_cart")
def add_to_cart_by_email(
    user_id: int = Query(...),
    category_id: int = Query(...),
    product_id: int = Query(...),
    quantity: int = Query(...),
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    existing_cart_item = (
            db.query(Cart)
            .filter(
                Cart.user_id == user.id,
                Cart.category_id == category_id,
                Cart.product_id == product_id
            )
            .first()
        )    
    if existing_cart_item:
        raise HTTPException(status_code =409 ,detail="Item already there in your cart")

    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    total_price = product.price * quantity

    cart_item = Cart(
        user_id=user.id,
        category_id = category.category_id,
        product_id=product.product_id,
        quantity=quantity,
        price_at_time=total_price
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return {"message": "Added to cart", "price_at_time": cart_item.price_at_time}


@router.get("/cart")
def get_cart_items(user_id: int = Query(...), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    cart_items = (
        db.query(Cart, Product)
        .join(Product, Cart.product_id == Product.product_id)
        .filter(Cart.user_id == user_id)
        .all()
    )

    result = []
    for cart, product in cart_items:
        result.append({
            "product_id": product.product_id,
            "category_id": cart.category_id,
            "product_name": product.product_name,
            "image_url": product.image_url,
            "price_per_unit": product.price,
            "quantity": cart.quantity,
            "price_at_time": cart.price_at_time,
        })

    return result


@router.patch("/cart/update_quantity")
def update_cart_quantity(
    user_id: int = Query(...),
    product_id: int = Query(...),
    quantity: int = Query(...),
    category_id:int =Query(...),
    db: Session = Depends(get_db)
):
    cart_item = (
        db.query(Cart)
        .filter(Cart.user_id == user_id,Cart.category_id == category_id, Cart.product_id == product_id )
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found.")

    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    cart_item.quantity = quantity
    cart_item.price_at_time = product.price * quantity

    db.commit()
    db.refresh(cart_item)

    return {"message": "Cart quantity updated successfully", "new_total": cart_item.price_at_time}
@router.delete("/delete_item")
def delete_item(    user_id: int = Query(...),
    product_id: int = Query(...),
    category_id:int =Query(...),
    db: Session = Depends(get_db)):
    cart_item = (
    db.query(Cart).filter(Cart.user_id == user_id,Cart.category_id == category_id, Cart.product_id == product_id ).first() )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found.")

    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    db.delete(cart_item)
    db.commit()
    return {"message": "Cart item deleted successfully"}


