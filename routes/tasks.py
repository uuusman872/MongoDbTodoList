from fastapi import APIRouter, HTTPException, status
from models.task import CreateTask, Task
from database.mongodb import task_collection
from helpers.task_helpers import task_helper
from bson import ObjectId
from validators.user_validator import validate_user_id
from validators.category_validator import validate_category_id
from fastapi import HTTPException, status
from typing import List
from fastapi import Query

router = APIRouter()
@router.post("/tasks", response_model=CreateTask)
async def create_task(task: CreateTask):
    tasks_data = task.dict()
    try:
        await validate_user_id(tasks_data.get("user_id"))
        for category_id in tasks_data.get("category_id"):
            await validate_category_id(category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    new_task = await task_collection.insert_one(tasks_data)
    created_task = await task_collection.find_one({"_id": new_task.inserted_id})
    return created_task


@router.get("/tasks")
async def get_all_task(page_number: int=1):
    tasks = []
    page_size = 10
    skip = (page_number - 1) * page_size
    async for task in task_collection.find().sort("due_date", -1).skip(skip).limit(page_size):
        tasks.append(task_helper(task))
    return tasks


@router.get("/task/{task_id}", response_model=Task)
async def get_task(task_id: str):
    task = await task_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
    return task_helper(task)


@router.get("/user_tasks/{user_id}")
async def get_tasks_by_user_id(user_id: str):
    task_list = []
    async for task in task_collection.find({"user_id": user_id}):
        task_list.append(task_helper(task))

    return task_list



@router.put("/task/{task_id}", response_model=Task)
async def update_task(task_id: str, task: Task):
    updated_task = await task_collection.find_one_and_update(
        {"_id": ObjectId(task_id)}, 
        {"$set": {
                "title": task.title, "description": task.description, 
                "due_date": task.due_date, "prioriy": task.prioriy
            }
        }
    )
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated_task


@router.delete("/task/{task_id}", response_model=dict)
async def delete_task(task_id: str):
    deleted_result = await task_collection.delete_one({"_id": ObjectId(task_id)})
    if deleted_result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": f"task {task_id} has been deleted"}


@router.get("/task_filter_tags")
async def task_stats(filter_tag: List[str] = Query(...), offset: int=0, limit: int=10):
    print("filters are ", filter_tag)
    cursor = task_collection.aggregate([
        {"$match": {"tags": {"$in": filter_tag}}},
        {"$skip": offset},
        {"$limit": limit}
    ])
    
    total_count = await task_collection.count_documents({"tags": {"$in": filter_tag}})

    tasks = []
    async for task in cursor:
        tasks.append(task_helper(task))
    
    return {
        "message": f"Found {len(tasks)} tasks with given tags.",
        "data": tasks,
        "status": status.HTTP_200_OK,
        "total": total_count,
    }


@router.get("/task_by_category")
async def task_by_category(category_tags: str):
    
    cursor = task_collection.aggregate([
        {
            "$lookup": {
                "from": "category",
                "let": {"task_categories": "$category_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$in": ["$_id", "$$task_categories"]
                            }
                        }
                    }
                ],
                "as": "matched_categories"
            }
        },
        {
            "$match": {
                "matched_categories.category_type": category_tags
            }
        }
    ])

    result = []
    async for category in cursor:
        print(category)

    return {
        "message": "",
        "data": result,
        "status": status.HTTP_200_OK
    }