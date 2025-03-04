import pymongo
from info import DATABASE_URI, DATABASE_NAME

class FilesDB:
    def __init__(self):
        self.client = pymongo.MongoClient(DATABASE_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db["files"]

    async def add_file(self, file_id, file_name):
        """Store file metadata in MongoDB."""
        await self.collection.update_one(
            {"file_name": file_name},
            {"$set": {"file_id": file_id, "file_name": file_name}},
            upsert=True
        )

    async def get_file(self, file_name):
        """Retrieve file metadata by name."""
        return await self.collection.find_one({"file_name": file_name})