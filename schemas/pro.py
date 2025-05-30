from pydantic import BaseModel
class Createproduct(BaseModel):
    product_name : str
    
    product_description : str
    category_id : int

    class Config:
        orm_mode = True

