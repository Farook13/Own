import pymongo

class GrantsDB:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["movie_bot"]
        self.collection = self.db["grants"]

    async def grant_access(self, user_id, permission):
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"permission": permission}},
            upsert=True
        )
