from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId as BsonObjectId
from models.pydanticObject import PydanticObjectId



class ActivityLog(BaseModel):
    id: PydanticObjectId
    task_id: PydanticObjectId
    user_id: PydanticObjectId
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)








