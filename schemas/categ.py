from pydantic import BaseModel
class Createcategory(BaseModel):
    category_id: int
    category_name: str
    image_url: str

    class Config:
        from_attributes = True 