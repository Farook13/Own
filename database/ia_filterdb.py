import pymongo

class InlineFilterDB:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["movie_bot"]
        self.collection = self.db["inline_filters"]

    async def add_inline_filter(self, query, result):
        await self.collection.insert_one({"query": query, "result": result})
