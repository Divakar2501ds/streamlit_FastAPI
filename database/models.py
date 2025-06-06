from sqlalchemy import create_engine,Column, Integer, String, Boolean, DateTime ,func ,ForeignKey,Float 
from datetime import datetime
from sqlalchemy.orm import sessionmaker ,declarative_base ,relationship ,Session 
from database.database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    email =  Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, unique=True, nullable=False)
    image_url = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "new_products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, unique=True, nullable=False)
    product_description = Column(String, nullable=True)
    price = Column(Float) 
    image_url = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("category.category_id"))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    category = relationship("Category", back_populates="products")

class Cart(Base):
    __tablename__ = "cart__items"
    cart_id = Column(Integer,primary_key=True ,index = True)
    user_id = Column (Integer, ForeignKey("user.id"))
    product_id = Column(Integer,ForeignKey("new_products.product_id"))
    category_id = Column(Integer,ForeignKey("category.category_id"))
    quantity = Column(Integer)
    price_at_time = Column(Float)
    user = relationship("User")
    product = relationship("Product")
    category = relationship("Category")