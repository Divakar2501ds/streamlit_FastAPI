from fastapi import UploadFile, File, Form, Depends, APIRouter ,HTTPException
from sqlalchemy.orm import Session
import shutil
from config import STATIC_DIR
import os
from auth.handler import get_current_user
from database import database
from database.models import Category
from database.models import Cart
router = APIRouter()


"""
For adding category 
if category already existed . it won't accept 
Input :
        category_name : str
        file : uploadfie
Output :
        category_name : str
        image_url :image_url
"""

@router.post("/add_category")
def add_category(
    category_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db) ,user: str = Depends(get_current_user)
):
    try:
        existing_category = db.query(Category).filter(Category.category_name == category_name).first()
        
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name already exists")
        else:
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
                "message": "Category added","data" :{"category_name":category_name,"image_url": image_url},"status_code":200 ,"user":user
            }
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e)) 








"""
For Displaying categories
Output :
        category_id :int
        category_name : str
        image_url : url


"""
@router.get("/categories")
def get_categories(db: Session = Depends(database.get_db) ,user: str = Depends(get_current_user)):
    db_category = db.query(Category).filter(Category.is_deleted.is_(False)).all()
    category_list = [ ]
    for cat in db_category:
            category_list.append(
            {"category_id":cat.category_id,
            "category_name":cat.category_name,
            "image_url":cat.image_url})
    return {
        "message":"categories list",
        "status_code":200,
        "data" :category_list ,
        "user":user
    }










"""

updating  category using category_id as path parameter
Input:
    category_name : str
    file : upload 

Output:
    category_id :int
    category_name: str
    image_url : url 

"""

@router.patch("/categories/{category_id}")
def update_category(
    category_id: int,
    category_name: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(database.get_db),
    user: str = Depends(get_current_user)
):  
    try:

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
        return {"message": "Category updated successfully","data":category, "status_code":200 ,"user":user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))








"""
Deleting Category using category_id as path parameter.
Suppose if the item is in the cart , it cannot be deleted
Input :
        categrory_id :int
Output:
       category deleted
"""
@router.delete("/delete_category/{category_id}") 
def delete_category(category_id: int, db: Session = Depends(database.get_db) ,user: str = Depends(get_current_user)): 
    try: 

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
        return {"category":category , "user":user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






"""
list of deleted categories 
Output :
        category_id :int
        category_name: str
        image_url : url 


"""
@router.get("/deleted_category")
def deleted_category(db: Session = Depends(database.get_db)):
    try:
        category = db.query(Category.category_name,Category.category_id ,Category.image_url).filter(Category.is_deleted == True).all()
        data = []
        for cat in category:
            deletedcategory = {
                "category_id":cat.category_id,
                "category_name": cat.category_name,
                "image_url": cat.image_url
            }
            data.append(deletedcategory)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
