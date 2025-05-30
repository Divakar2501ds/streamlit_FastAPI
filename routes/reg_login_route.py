from fastapi import FastAPI, HTTPException, Depends,Request ,APIRouter
from sqlalchemy.orm import Session
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY,HTTP_401_UNAUTHORIZED
from database import models
from database import database
from schemas import reg_login
from passlib.context import CryptContext
from typing import List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



router = APIRouter()

@router.post("/register")
def create_user(user: reg_login.UserCreate, db: Session = Depends(database.get_db)): 
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, role=user.role, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "id": db_user.id,
        "email": db_user.email,
        "role": db_user.role
    }


@router.get("/users/", response_model=List[reg_login.UserCreate])
def list_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return [
        reg_login.UserCreate(
            email=user.email,
            password="***",  
            role=user.role
        ) for user in users
    ]
@router.get("/geti{a}")
def info(a:str):
    for i in reg_login.UserCreate:
        if i[ "email"] == a:
            return {"data":i}
  
@router.post("/login")
def login(user: reg_login.userlogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
        }
    }



