import pymongo

class UsersChatsDB:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["movie_bot"]
        self.collection = self.db["users_chats"]

    async def add_user_chat(self, user_id, chat_id):
        await self.collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"chat_ids": chat_id}},
            upsert=True
        )
