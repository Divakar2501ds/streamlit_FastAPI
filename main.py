from fastapi import FastAPI
from routes import category_route
from routes import product_route
from routes import reg_login_route
from routes import Cart_route , protected
from config import STATIC_DIR
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(reg_login_route.router)
app.include_router(category_route.router)
app.include_router(product_route.router)
app.include_router(Cart_route.router)
app.include_router(protected.router)