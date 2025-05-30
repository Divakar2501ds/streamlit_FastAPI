from fastapi import FastAPI, UploadFile, File, Form, Depends ,APIRouter ,HTTPException
from sqlalchemy.orm import Session
import shutil
from PIL import Image ,ImageOps
import io
import os
from typing import List
from database import database
from database.models import Category
from database.models import Cart
from schemas.categ import Createcategory
from fastapi.staticfiles import StaticFiles


app = FastAPI()


router = APIRouter()

@router.post("/add_category")
def add_category(
    category_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    existing = db.query(Category).filter(Category.category_name == category_name).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Category name already exists")
    else:
        STATIC_DIR = "/home/ib-40/Downloads/newregister/static"
        os.makedirs(STATIC_DIR, exist_ok=True)

        image_path = os.path.join(STATIC_DIR, file.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_url = f"/static/{file.filename}"
        new_cat = Category(category_name=category_name, image_url=image_url)
        db.add(new_cat)
        db.commit()
        db.refresh(new_cat)

        return {
            "message": "Category added",
            "image_url": image_url
        }

@router.get("/categories", response_model=List[Createcategory])
def get_categories(db: Session = Depends(database.get_db)):
    return db.query(Category).filter(Category.is_deleted.is_(False)).all()

@router.patch("/categories/{category_id}")
def update_category(
    category_id: int,
    category_name: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(database.get_db)
):
    category = db.query(Category).filter(Category.category_id == category_id, Category.is_deleted == False).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_name and category_name != category.category_name:
        existing = db.query(Category).filter(Category.category_name == category_name, Category.is_deleted == False).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category name already exists")
        category.category_name = category_name
    if file:
        image_path = f"static/{file.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        category.image_url = f"/static/{file.filename}"


    db.commit()
    db.refresh(category)
    return {"message": "Category updated successfully"}


@router.delete("/delete_category/{category_id}") 
def delete_category(category_id: int, db: Session = Depends(database.get_db)): 
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category_in_cart = db.query(Cart).filter(Cart.category_id == category_id).first()
    if category_in_cart:
        raise HTTPException(
            status_code=409, 
            detail="Cannot delete this category because it is present in a cart."
        )


    category.is_deleted = True
    db.commit()
    return category

@router.get("/deleted_category")
def deleted_category(db: Session = Depends(database.get_db)):
    category = db.query(Category.category_name,Category.category_id ,Category.image_url).filter(Category.is_deleted == True).all()
    data = []
    for cat in category:
        deletedcategory = {
            "category_id ":cat.category_id,
            "category_name": cat.category_name,
            "image_url": cat.image_url
        }
        data.append(deletedcategory)
    return data