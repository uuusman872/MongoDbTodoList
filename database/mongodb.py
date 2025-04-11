from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.test_db
user_collection = db.get_collection("users")


def user_helper(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "created_at": user["created_at"]
    }

