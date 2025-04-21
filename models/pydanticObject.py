from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel


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