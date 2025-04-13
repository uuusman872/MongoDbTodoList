from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId as BsonObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),  # show as string in OpenAPI
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

    @classmethod
    def validate(cls, v, _info=None):
        if isinstance(v, BsonObjectId):
            return v
        if not BsonObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return BsonObjectId(v)


class CreateTask(BaseModel):
    title: str = Field(...) # required Field
    description: Optional[str]
    due_date: Optional[datetime]
    update_date: Optional[datetime]
    prioriy: Optional[int] = 1
    completed: bool
    user_id: PydanticObjectId
    category_id: Optional[list[PydanticObjectId]] = []

    class Config:
        schema_extra = {
            "example": {
                "title": "Finish FastApi Project",
                "description": "Implemen MongoDB Integration and routes",
                "due_date": "2025-04-12T15:00:00",
                "priority": 3,
                "user_id": "user_id"
            }
        }


class Task(BaseModel):
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    update_date: Optional[datetime]
    prioriy: Optional[int] = 1
    completed: bool
    user_id: PydanticObjectId # requires the pydanticObjectId Validator
    category_id: Optional[list[PydanticObjectId]] = []




