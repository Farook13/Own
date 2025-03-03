import pymongo
import os

class ConnectionsDB:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
        self.db = self.client["movie_bot"]
        self.collection = self.db["connections"]

    async def add_connection(self, user_id, chat_id):
        await self.collection.insert_one({"user_id": user_id, "chat_id": chat_id})

    async def get_connection(self, user_id):
        return await self.collection.find_one({"user_id": user_id})
