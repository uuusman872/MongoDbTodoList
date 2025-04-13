from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId as BsonObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema






class Category_Create(BaseModel):
    category_type: str
    




