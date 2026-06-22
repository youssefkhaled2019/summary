from fastapi.schemas import BaseModel,Field

class User(BaseModel):
    name: str
    age: int
    username: str = Field(min_length=3) #Validation
    age: int = Field(gt=0)