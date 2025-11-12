# test_mongo_connection.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env
load_dotenv()

def get_mongodb_client():
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        print("⚠️ MONGODB_URI not set, using local storage")
        return None
    
    try:
        client = MongoClient(mongodb_uri)
        # Test connection
        client.admin.command('ping')
        print("✓ Connected to MongoDB Atlas")
        return client
    except Exception as e:
        print(f"⚠️ MongoDB connection failed: {e}")
        return None

if __name__ == "__main__":
    get_mongodb_client()
