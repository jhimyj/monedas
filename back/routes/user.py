from fastapi import APIRouter, HTTPException
from dataclasses import dataclass
from utility.db_connector import DbConnector

router = APIRouter()

@dataclass
class User:
    name: str
    email: str
    password: str

user_db = DbConnector(path="db/user.json", key_attribute="id")

# Gets user info by their ID
@router.get("/user/{user_id}")
def get_user(user_id: int):
    user = user_db.get_one_by_attribute(attribute_name="id", attribute_value=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Creates a user
@router.post("/user/")
def create_user(user: User):
    # if user email already exists
    if user_db.get_one_by_attribute(attribute_name="email", attribute_value=user.email) is not None:
        raise HTTPException(status_code=400, detail="User with said email already exists")
    
    result = user_db.insert_into_table(key_attribute="id", value=user)
    if not result:
        raise HTTPException(status_code=500, detail="Could not insert into db")
    return user