


def user_helper(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }



def user_task_helper(user):
    data = {
         "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
        "tasks_list": []
    }

    for task in user["tasks_list"]:
        data["tasks_list"].append({
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "due_date": task["due_date"],
        "update_date": task["update_date"],
        "prioriy": task["prioriy"],
        "user_id": task["user_id"],
        "tags": task["tags"],
        "category_id": task["category_id"],
        "parent_task_id": task["parent_task_id"]
    })
    return data