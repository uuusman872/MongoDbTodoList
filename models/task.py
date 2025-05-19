from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId as BsonObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import List
from models.pydanticObject import PydanticObjectId
from pydantic import field_validator
from database.mongodb import user_collection
from bson import ObjectId
from typing import Literal

class CreateTask(BaseModel):
    title: str = Field(...) # required Field
    description: Optional[str]
    due_date: Optional[datetime]
    update_date: Optional[datetime]
    prioriy: Literal["high", "medium", "low"] = "low"
    completed: bool
    user_id: PydanticObjectId
    category_id: Optional[list[PydanticObjectId]] = []
    parent_task_id: Optional[PydanticObjectId] = None
    reminder_time: Optional[datetime] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    is_recurring: bool = False
    estimated_duration_minutes: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Finish FastApi Project",
                "description": "Implemen MongoDB Integration and routes",
                "due_date": "2025-04-12T15:00:00",
                "priority": 3,
                "user_id": "user_id",
                "category_id": [],
                "parent_task_id": "",
                "tags": []

            }
        }


class Task(BaseModel):
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    update_date: Optional[datetime]
    prioriy: Literal["high", "medium", "low"] = "low"
    completed: bool
    user_id: PydanticObjectId # requires the pydanticObjectId Validator
    category_id: Optional[list[PydanticObjectId]] = []
    tags: Optional[List[str]] = Field(default_factory=list)
    parent_task_id: Optional[PydanticObjectId] = None





