import pymongo

class JoinRequestsDB:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["movie_bot"]
        self.collection = self.db["join_requests"]

    async def add_join_request(self, user_id, chat_id):
        await self.collection.insert_one({"user_id": user_id, "chat_id": chat_id})
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​id})
