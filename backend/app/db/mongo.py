from pymongo import MongoClient
from app.core.config import settings

class MongoDB:
    client: MongoClient = None
    db = None
    collection = None

    @classmethod
    def connect(cls):
        if cls.client is None:
            cls.client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
            # Verify connection
            try:
                cls.client.server_info()
                print(f"DTO Connected to MongoDB at {settings.MONGO_URI.split('@')[-1] if '@' in settings.MONGO_URI else 'localhost'}")
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                raise e
            
            cls.db = cls.client[settings.MONGO_DB_NAME]
            cls.collection = cls.db["user_recommendations"]
    
    @classmethod
    def close(cls):
        if cls.client:
            cls.client.close()

mongo_db = MongoDB()
