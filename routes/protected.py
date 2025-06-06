from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer 
from auth.handler import get_current_user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()


@router.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    return {"message": f"Hello, {user}"}         
