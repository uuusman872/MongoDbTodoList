from database.mongodb import category_collection
from bson import ObjectId

async def validate_category_id(category_id):
    id = await category_collection.find_one({"_id": ObjectId(category_id)})
    if not id:
        raise ValueError(f"category {category_id} not found")
    return id