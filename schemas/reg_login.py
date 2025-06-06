from pydantic import BaseModel ,EmailStr

class UserCreate(BaseModel):
    role: str
    email: EmailStr
    password: str
    
class userlogin(BaseModel):
    email : EmailStr
    password : str
