from fastapi import FastAPI,status
from pydantic import BaseModel,EmailStr ,Field
from typing import Optional
app=FastAPI()

class Owner(BaseModel):
   name:str
   email:EmailStr
class Product(BaseModel):
    title:str=Field(min_length=3,max_length=20)
    price:int=Field(gt=0,le=100)
    tags:Optional[list[str]]=[]
    owner:Optional[Owner]=None
@app.get("/")
def hoem():
    return {"message": "welcome"}

@app.post("/",status_code=status.HTTP_201_CREATED)
def home(pro:Product):
    return pro


# {
#   "title": "FastAPI",
#   "price": 50,
#   "tags": ["python", "backend"],
#   "owner": {
#     "name": "Ahmed",
#     "email": "ahmed@gmail.com"
#   }
# }
# --------------------------------------------