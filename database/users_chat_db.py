import pymongo
from info import DATABASE_URI

class UsersChatsDB:
    def __init__(self):
        self.client = pymongo.MongoClient(DATABASE_URI)
        self.db = self.client["pcmovies"]  # Matches DATABASE_NAME from info.py
        self.collection = self.db["users_chats"]  # Collection for user-chat data

    async def add_user_chat(self, user_id, chat_id):
        await self.collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"chat_ids": chat_id}},
            upsert=True
        )

    async def get_user_chats(self, user_id):
        result = await self.collection.find_one({"user_id": user_id})
        return result["chat_ids"] if result else []