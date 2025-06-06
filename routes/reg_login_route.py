from fastapi import HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from starlette import status
from database import models
from database import database
from schemas import reg_login
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config import SECRET_KEY , ALGORITHM
from typing import Annotated
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()
"""
    Registering new user , if user already exist it shows email already registered

    Input:
        - role : str
        - email : emailstr
        - password : str
    Output:
        - id: int
        - email: str
        - role : str

    """
@router.post("/register")
def create_user(user: reg_login.UserCreate, db: Session = Depends(database.get_db)): 

    try :

        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code= 400, detail="Email already registered")
        

        hashed_pw = pwd_context.hash(user.password)
        db_user = models.User(email=user.email, role=user.role, hashed_password=hashed_pw)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            "data":{
                "id": db_user.id,
                "email": db_user.email,
                "role": db_user.role
                },
            "message": "User Register successfully",
            "status_code" : 200,
        }
    except Exception as e:
        return {
            "Detail": f"unable to process the request {e}"
        }
    


"""
function to create access token
"""
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



# To get particular user details using path parameters
@router.get("/geti/{a}")
def info(a:str):
    for i in reg_login.UserCreate:
        if i[ "email"] == a:
            return {"data":i}
        

""" Login using Post method()  
How it works using post method - if input email exists in db .
Input :
       email - Emailstr
       password - str
Output :

        userid = int
        email = EmailStr
        status_code = 200 
 
"""
@router.post("/login")
def login(user: reg_login.userlogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer","user_id":db_user.id}

