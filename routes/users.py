from fastapi import APIRouter, HTTPException
from models.user import User, UserCreate
from database.mongodb import user_collection, user_helper
import bcrypt
from datetime import datetime

router = APIRouter()

@router.post("/users", response_class=User)
async def create_user(user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "full_name": user.full_name,
        "created_at": datetime.utcnow()
    }
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    