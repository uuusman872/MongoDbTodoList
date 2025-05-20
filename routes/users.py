from fastapi import APIRouter, HTTPException, status
from models.user import User, UserCreate, UpdateUser
from database.mongodb import user_collection
import bcrypt
from datetime import datetime
from bson import ObjectId
from helpers.user_helpers import user_helper, user_task_helper

router = APIRouter()

@router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "full_name": user.full_name,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    result = await user_collection.insert_one(new_user)
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    return user_helper(created_user)


@router.get("/users", response_model=list[User])
async def get_all_users(page_number: int = 1):
    users = []
    page_size = 10
    skip = (page_number - 1) * page_size
    total_records = await user_collection.count_documents({})
    print("[+] The total number of records are ", total_records)
    async for user in user_collection.find().sort("created_at", -1).skip(skip).limit(page_size):
        users.append(user_helper(user))
    return users



@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)



@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UpdateUser):
    updated_user = await user_collection.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": {"full_name": user.full_name, "email": user.email, "updated_at": datetime.utcnow()}}, return_document=True)
    if not updated_user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user_helper(updated_user)



@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    deleted_result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    if deleted_result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return {"message": f"user {user_id} has been deleted"}



@router.get("/user_tasks/{user_id}")
async def user_task_progress(user_id: str):
    cursor = user_collection.aggregate([
            {
                "$match": { "_id": ObjectId(user_id) }
            },
            {
                "$addFields": {
                    "_id": { "$toString": "$_id" }
                }
            },
            {
                "$lookup": {
                    "from": "tasks",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "tasks_list"
                }
            }
        ])
    
    users_tasks = []
    
    async for user in cursor:
        users_tasks.append(user_task_helper(user))
    
    return {
        "message": "", 
        "status": status.HTTP_200_OK,
        "data": users_tasks
    }