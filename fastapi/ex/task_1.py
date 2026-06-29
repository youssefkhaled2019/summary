"""
مشروع صغير للتدريب

نفّذ API بالمواصفات التالية:

Create User
{
    "name": "Youssef",
    "age": 25
}
Validation
name ≥ 3 أحرف
age بين 1 و 120
Errors
المستخدم غير موجود → 404
البيانات غير صحيحة → 422 (FastAPI يعالجها تلقائيًا)
Success
POST → 201
GET → 200
DELETE → 204 أو 200
"""


from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# =========================
# Schemas
# =========================

class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=1, le=120)


class UserResponse(BaseModel):
    id: int
    name: str
    age: int


# =========================
# Fake Database
# =========================

users: List[UserResponse] = []
counter = 1


# =========================
# Create User
# POST -> 201
# =========================

@app.post("/users",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global counter
    new_user = UserResponse(    id=counter,    name=user.name,    age=user.age )
    users.append(new_user)
    counter += 1
    return new_user


# =========================
# Get All Users
# GET -> 200
# =========================

@app.get("/users",  response_model=List[UserResponse],  status_code=status.HTTP_200_OK)
def get_users():
    return users


# =========================
# Get User By ID
# GET -> 200
# Not Found -> 404
# =========================

@app.get( "/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found" )
# =========================
# Delete User
# DELETE -> 204
# Not Found -> 404
# =========================
@app.delete( "/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return Response(   status_code=status.HTTP_204_NO_CONTENT    )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found" )