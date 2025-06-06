
from fastapi import  UploadFile, File, Form, Depends ,APIRouter ,HTTPException
from sqlalchemy.orm import Session
import shutil
from config import STATIC_DIR
import os
from auth.handler import get_current_user
from database import database
from database.models import Product 
import shutil

router = APIRouter()





"""
Add product 
    Input:
        product_name: str
        product_description: str
        price: int
        category_id:int
        file: UploadFile
    Output:
        product_name: str
        product_description: str
        price: int
        category_id:int
        image_url : url

"""
@router.post("/add_product")
def add_product(
    product_name: str = Form(...),
    product_description: str = Form(...),
    price: int = Form(...),
    category_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),user: str = Depends(get_current_user)
):
    try :
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

        return {"message": "Product added" ,"data":new_product , "status_code":200 ,"user":user }

    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
    



""""
getting products based on category using category_id
Input:
    category_id : int

Output:
        product_name: str
        product_description: str
        price: int
        category_id:int
        image_url : url

    
"""
@router.get("/products/category/{category_id}")
def get_products_by_category(category_id: int, db: Session = Depends(database.get_db),user: str = Depends(get_current_user)):
    try:
        products = db.query(Product).filter(Product.category_id == category_id).all()
        return {"message": "products","data":products, "status_code":200,"user":user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



""""
Getting product  details based on product_id 
Input:
    product_id : int 
Output:
        product_name: str
        product_description: str
        price: int
        category_id:int
        image_url : url

"""
@router.get("/products/product/{product_id}")
def get_product_details_by_product(product_id: int, db: Session = Depends(database.get_db),user: str = Depends(get_current_user)):
    try:
        products = db.query(Product).filter(Product.product_id == product_id).first()
        return {"message": "products","data":products, "status_code":200,"user":user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



"""
Deleting product using product id 
Input:
    product_id : int 
Output:
        deleted 

"""

@router.delete("/delete_product/{product_id}") 
def delete_product(product_id: int, db: Session = Depends(database.get_db),user: str = Depends(get_current_user)): 
    try:
            
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="product not found")
        product.is_deleted = True
        db.commit()
        return {"message": "Product deleted", "data":product, "status_code":200,"user":user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



"""
update product 
    Input:
        product_name: str
        product_description: str
        price: int
        product_id:int
        file: UploadFile
    Output:
        product_name: str
        product_description: str
        price: int
        product_id:int
        image_url : url

"""

@router.patch("/update_product/{product_id}")
def update_product(
product_id: int,
product_name: str = Form(...),
product_description: str = Form(...),
price: int = Form(...),
file: UploadFile = File(None), 
db: Session = Depends(database.get_db),
user: str = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    try:
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if file:
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

            db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Product updated successfully"}
