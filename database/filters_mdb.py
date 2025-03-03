import pymongo

class FiltersDB:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["movie_bot"]
        self.collection = self.db["filters"]

    async def add_filter(self, chat_id, filter_name):
        await self.collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"filter_name": filter_name}},
            upsert=True
        )
