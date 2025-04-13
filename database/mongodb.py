from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.test_db


user_collection = db.get_collection("users")
task_collection = db.get_collection("tasks")
category_collection = db.get_collection("category")
