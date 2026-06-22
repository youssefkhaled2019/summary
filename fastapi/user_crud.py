
from fastapi import FastAPI
app=FastAPI()

from fastapi.schemas import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int


users = []    

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return user

@app.get("/users",response_model=[User])
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    # for user in users:
    #     if user.id == user_id:
    #         return user
    try:
        return  users[user_id]
    except:
        return {"message": "User not found"}

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    # for index, user in enumerate(users):
    #     if user.id == user_id:
    #         users[index] = updated_user
    #         return updated_user
    try:
        users[user_id] = updated_user
        return  users[user_id]
    except:
        return {"message": "User not found"}
    
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # for index, user in enumerate(users):
    #     if user.id == user_id:
    #         users.pop(index)
    #         return {"message": "Deleted"}
    try:
        users.pop(user_id)
        return {"message": "Deleted"}
    except:
        return {"message": "User not found"}
