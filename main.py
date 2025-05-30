from fastapi import FastAPI
from routes import category_route
from routes import product_route
from routes import reg_login_route
from routes import Cart_route
from database.database import Base, engine
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="/home/ib-40/Downloads/newregister/static"), name="static")
Base.metadata.create_all(bind=engine)
app.include_router(reg_login_route.router)
app.include_router(category_route.router)
app.include_router(product_route.router)
app.include_router(Cart_route.router)


