
from fastapi import FastAPI, UploadFile, File, Form, Depends ,APIRouter ,HTTPException ,Query
from sqlalchemy.orm import Session
import shutil
from PIL import Image , ImageOps
import os
from typing import List 
from database import database
from database.models import Product 
from schemas.pro import Createproduct 
from fastapi.staticfiles import StaticFiles
import shutil
app = FastAPI()

router = APIRouter()




@router.post("/add_product")
def add_product(
    product_name: str = Form(...),
    product_description: str = Form(...),
    price: int = Form(...),
    category_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    try :
        STATIC_DIR = "/home/ib-40/Downloads/newregister/static"
        os.makedirs(STATIC_DIR, exist_ok=True)

        image_path = os.path.join(STATIC_DIR, file.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_url = f"/static/{file.filename}"
        new_product = Product(
            product_name=product_name,
            product_description=product_description,
            price=price,
            category_id=category_id,
            image_url=image_url
        )
        db.add(new_product)
        db.commit()

        return {"message": "Product added"}

    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
@router.get("/get_product")
def get_product(db: Session = Depends(database.get_db)):
    productlist = db.query(
        Product.product_name,
        Product.price ,
        Product.category_id,
        Product.product_description,
        Product.image_url
    ).all()

    data = [
        {
            "product_name": pro.product_name,
            "price":pro.price,
            "product_description": pro.product_description,
            "image_url": pro.image_url,
        }
        for pro in productlist
    ]

    return data

@router.get("/products/category/{category_id}")
def get_products_by_category(category_id: int, db: Session = Depends(database.get_db)):
    products = db.query(Product).filter(Product.category_id == category_id).all()
    return products



@router.get("/products/product/{product_id}")
def get_product_details_by_product(product_id: int, db: Session = Depends(database.get_db)):
    products = db.query(Product).filter(Product.product_id == product_id).first()
    return products


@router.delete("/delete_category/{product_id}") 
def delete_category(product_id: int, db: Session = Depends(database.get_db)): 
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    product.is_deleted = True
    db.commit()
    return {"message": "Category deleted"}


@router.patch("/update_product/{product_id}")
def update_product(
product_id: int,
product_name: str = Form(...),
product_description: str = Form(...),
price: int = Form(...),
category_id: int = Form(...),
file: UploadFile = File(None), 
db: Session = Depends(database.get_db)
):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    try:
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if file:
            STATIC_DIR = "/home/ib-40/Downloads/newregister/static"
            os.makedirs(STATIC_DIR, exist_ok=True)

            image_path = os.path.join(STATIC_DIR, file.filename)
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            product.image_url = f"/static/{file.filename}"
        if product_name is not None:
            product.product_name = product_name

        if product_description is not None:
            product.product_description = product_description

        if price is not None:
            product.price = price

        if category_id is not None:
            product.category_id = category_id

            db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Product updated successfully"}
