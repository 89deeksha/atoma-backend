from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str


@ app.get("/")
def read_root():
    return{"message":"hello world"}

@ app.post("/users")
def create_user(user: User):
    return {
        "name": user.name,
        "email": user.email
    }