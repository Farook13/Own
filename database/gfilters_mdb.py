import pymongo

class GroupFiltersDB:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["movie_bot"]
        self.collection = self.db["group_filters"]

    async def add_group_filter(self, group_id, filter_key):
        await self.collection.update_one(
            {"group_id": group_id},
            {"$set": {"filter_key": filter_key}},
            upsert=True
        )
