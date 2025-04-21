from database.mongodb import user_collection
from bson import ObjectId

async def validate_user_id(user_id):
    user_id = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user_id:
        raise ValueError(f"user_id {user_id} not found")
    return user_id