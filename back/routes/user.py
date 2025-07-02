from fastapi import APIRouter, HTTPException, Body
from dataclasses import dataclass
from utility.db_connector import DbConnector

@dataclass
class User:
    name: str
    email: str
    password: str

class UserRouter:
    def __init__(self, user_db: DbConnector):
        self.user_db = user_db
        
        self.router = APIRouter()
        self.router.post("/user/login/")(self.log_in_user)
        self.router.get("/user/{user_id}")(self.get_user)
        self.router.post("/user/")(self.create_user)

    def log_in_user(self, body: dict = Body(...)):
        email = body.get("email")
        password = body.get("password")
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")
        user = self.user_db.get_one_by_attribute(attribute_name="email", attribute_value=email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user["password"] != password:
            raise HTTPException(status_code=401, detail="Incorrect password")
        return user

    # Gets user info by their ID
    def get_user(self, user_id: int):
        user = self.user_db.get_one_by_attribute(attribute_name="id", attribute_value=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    # Creates a user
    def create_user(self, user: User):
        # if user email already exists
        if self.user_db.get_one_by_attribute(attribute_name="email", attribute_value=user.email) is not None:
            raise HTTPException(status_code=400, detail="User with said email already exists")
        
        result = self.user_db.insert_into_table(key_attribute="id", value=user)
        if not result:
            raise HTTPException(status_code=500, detail="Could not insert into db")
        return user