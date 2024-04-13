import motor.motor_asyncio
from bson.objectid import ObjectId 

MONGO_DETAILS = "mongodb://mongo:27017/"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.user

user_collection = database.get_collection("users_collection")



class UserRepository:

    def userData(data) -> dict:
        return {
            "id": str(data["_id"]),
            "username": data["username"],
            "name": data["name"],
            "country": data["country"],
            "phone": data["phone"],
            "adress": data["adress"],
            "email": data["email"],
            "password": data["password"],
            "role": data["role"]
            
        }
        
    def userDataView(data) -> dict:
        return {
            "id": str(data["_id"]),
            "username": data["username"],
            "name": data["name"],
            "country": data["country"],
            "phone": data["phone"],
            "adress": data["adress"],
            "email": data["email"],
            "role": data["role"]
        }



