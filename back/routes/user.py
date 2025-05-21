from fastapi import APIRouter, HTTPException
from dataclasses import dataclass
from utility.db_connector import DbConnector

router = APIRouter()

@dataclass
class User:
    id: int
    name: str
    email: str
    password: str

user_db = DbConnector("db/user.json")

@router.get("/user/{user_id}")
def get_user(user_id: int):
    user = user_db.get_one_by_attribute("id", user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user/")
def create_user(user: User):
    # if user id already exists
    if user_db.get_one_by_attribute("id", user.id) is not None:
        raise HTTPException(status_code=400, detail="User with said ID already exists")
    # if user email already exists
    if user_db.get_one_by_attribute("email", user.email) is not None:
        raise HTTPException(status_code=400, detail="User with said email already exists")
    
    result = user_db.insert_into_table(user)
    if not result:
        raise HTTPException(status_code=500, detail="Could not insert into db")
    return user