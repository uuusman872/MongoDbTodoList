
def task_helper(task):
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "due_date": task["due_date"],
        "update_date": task["update_date"],
        "prioriy": task["prioriy"],
        "user_id": task["user_id"],
        "category_id": task["category_id"],
        "parent_task_id": task["parent_task_id"]
    }

