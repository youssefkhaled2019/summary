
from fastapi import FastAPI
from typing import List
app=FastAPI()

# from fastapi.schemas import BaseModel
from typing import Optional
from pydantic import BaseModel 
class User(BaseModel):
    id: Optional[int]=None
    name: str
    age: int


users = []    
counter=0
@app.post("/users")
def create_user(user: User):

    # global counter 
    # user.id=counter+1
    # counter+=1
    
    # user_dict = user.model_dump()
    # user_dict["id"] = counter

    users.append(user)
    return user

@app.get("/users",response_model=List[User])
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    # try:
    #     return  users[user_id]
    # except:
    #     return {"message": "User not found"}

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            updated_user.id=user_id
            users[index] = updated_user
            return updated_user
    # try:
    #     users[user_id] = updated_user # {"id": user_id, "user": user}
    #     return  users[user_id]
    # except:
    #     return {"message": "User not found"}
    
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return {"message": "Deleted"}
    # try:
    #     users.pop(user_id)
    #     return {"message": "Deleted"}
    # except:
    #     return {"message": "User not found"}

# ----------------------------------
#user /database.py
# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///app.db"
# DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/mydb" #PostgreSQL
                 #"mysql+pymysql://user:password@localhost/db_name" #MySQL
# Engine
engine = create_engine(DATABASE_URL,echo=True) #مسؤول عن الاتصال بقاعدة البيانات.
"""
echo=True يجعل SQLAlchemy يطبع SQL في الـ Terminal.
"""


# Session Factory
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

# Base Class
class Base(DeclarativeBase):
    pass

# Dependency for FastAPI
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


#user /models.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True )
    name: Mapped[str] = mapped_column( String(100))
    email: Mapped[str] = mapped_column(  String(255), unique=True )

#user/schemas.py

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    name: str
    email: EmailStr

# main.py

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI
app=FastAPI()

@app.post("/users")
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    # db_user = User( name=user.name, email=user.email )
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    # return db_user
    return create_user( db, user)

@app.get("/users")
def get_users( db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}")
def get_user(user_id: int,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    # user = db.get( User,user_id) #SQLAlchemy 2.0
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int,data: UserUpdate,db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        return {"message": "Not Found" }
    user.name = data.name
    user.email = data.email
    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int,db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        return { "message": "Not Found" }
    db.delete(user)
    db.commit()
    return { "message": "Deleted"}


# user /crud.py
def create_user(db: Session, user: UserCreate):
    db_user = User( name=user.name, email=user.email  )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# =======================
# users = db.query(User).filter( User.name == "Ahmed").all()

# users = db.query(User).filter(User.name == "Ahmed", User.email == "a@gmail.com").all()
# users = db.query(User).order_by(User.id.desc()).all()
# user = db.query(User).first()
# count = db.query(User).count()