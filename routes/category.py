from fastapi import APIRouter, HTTPException, status
from models.categories import Category_Create
from database.mongodb import category_collection
from helpers.category_helper import category_helper
from bson import ObjectId

router = APIRouter()

@router.post("/category")
async def create_category(category: Category_Create):
    category = await category_collection.insert_one(category.dict())
    new_category = await category_collection.find_one({"_id": category.inserted_id})
    return category_helper(new_category)


@router.get("/category")
async def get_categories_list():
    category_list = []
    async for category in category_collection.find():
        category_list.append(category_helper(category))
    return category_list


@router.get("/category/{category_id}")
async def get_category(category_id):
    category = await category_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Not found")
    return category_helper(category)


@router.put("/category/{category_id}")
async def category_update(category_id: str, update_category: Category_Create):
    category_update = await category_collection.find_one_and_update(
        {"_id": ObjectId(category_id)}, 
        {"$set": {"category_type": update_category["category_type"]}}
    )
    
    if not category_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return category_update


@router.delete("/category/{category_id}")
async def category_delete(category_id: str):
    deleted_result = await category_collection.delete_one({"_id": ObjectId(category_id)})
    if deleted_result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
    return {"message": f"user {category_id} has been deleted"}
