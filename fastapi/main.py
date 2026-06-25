from fastapi import FastAPI
from fastapi.schemas import User,UserResponse
from fastapi import status
from fastapi import Depends

app = FastAPI()


# ===================================
@app.get("/users")
def get_users():pass

@app.post("/users")
def create_user():pass

@app.put("/users/1")
def update_user():    return {"message": "User updated"}

@app.delete("/users/1")
def delete_user():pass
# ===================================





@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

#Path Parameters 
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

#Query Parameters /users?page=2&limit=5
@app.get("/users") 
def get_users(page: int = 1, limit: int = 10):
    return {"page": page, "limit": limit}

# Request Body + Pydantic
@app.post("/users" ,response_model=UserResponse,status_code=status.HTTP_201_CREATE)# response_model=List[UserResponse]
def create_user(user: User):#<----Request Body 
    # user.username
    # user.model_dump() #json to Dictionary
    # user.model_dump_json() Dictionary to  json
    return user





# -------------------
def get_db():
    return "db"

@app.get("/")
def home(db = Depends(get_db)): #Dependency Injection
    return db

# -------------------
# router.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def get_users():
    pass


# main.py
app.include_router(router)

# -------------------
from app.database import engine
from app.database import Base

Base.metadata.create_all( bind=engine)

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users