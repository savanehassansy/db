import motor.motor_asyncio
from bson.objectid import ObjectId 
from repositories.user_repository import UserRepository

MONGO_DETAILS = "mongodb://mongo:27017/"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.user

user_collection = database.get_collection("users_collection")


# Retrieve all students present in the database
async def all_users():
    user = []
    async for data in user_collection.find():
        user.append(UserRepository.userDataView(data))
    return user


# Add a new student into to the database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    print(user)
    new_user= await user_collection.find_one({"_id": user.inserted_id})
    return UserRepository.userData(new_user)


# Retrieve a student with a matching ID
async def get_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return UserRepository.userDataView(user)
    
# Delete a student from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True

