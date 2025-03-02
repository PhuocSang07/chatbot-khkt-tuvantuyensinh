from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, config):
        self.client = MongoClient(config.MONGODB_ATLAS_CLUSTER_URI)
        self.db = self.client[config.DB_NAME]
        self.collection = self.db[config.COLLECTION_NAME]
        print(f"Kết nối database thành công: {self.db.name}")