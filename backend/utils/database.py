import os
from pymongo import MongoClient
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ==========================================================
# 🧠 MongoDB Connection Setup
# ==========================================================

def get_mongodb_client():
    """
    Establish and return a MongoDB Atlas client.
    Reads URI from environment variable MONGODB_URI.
    """
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        print("⚠️ MONGODB_URI not set. Please check your .env file.")
        return None

    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        # Ping the server to verify connection
        client.admin.command('ping')
        print("✓ Connected to MongoDB Atlas")
        return client
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None


# ==========================================================
# 💾 Save Simplification History
# ==========================================================

def save_document_history(user_session, original_text, simplified_text, filename=None):
    """
    Save the document simplification record to MongoDB.
    Returns the inserted document ID if successful, else None.
    """
    client = get_mongodb_client()
    if not client:
        print("⚠️ No MongoDB client. Skipping insert.")
        return None

    try:
        db = client["legal_documents"]     # Database name
        collection = db["history"]         # Collection name

        history_entry = {
            "user_session": user_session or "unknown_user",
            "original_text": original_text[:500],   # Store only first 500 chars
            "simplified_text": simplified_text[:500],
            "filename": filename,
            "timestamp": datetime.utcnow(),
            "status": "completed"
        }

        print("🟡 Attempting to insert document into MongoDB...")
        result = collection.insert_one(history_entry)
        print(f"✅ MongoDB insert success! Document ID: {result.inserted_id}")

        client.close()
        return str(result.inserted_id)

    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
        return None


# ==========================================================
# 📜 Fetch Simplification History
# ==========================================================

def get_user_history(user_session, limit=10):
    """
    Fetch recent simplification history for a user from MongoDB.
    Returns a list of document dicts.
    """
    client = get_mongodb_client()
    if not client:
        print("⚠️ No MongoDB client. Returning empty list.")
        return []

    try:
        db = client["legal_documents"]
        collection = db["history"]

        print(f"🔍 Fetching last {limit} history items for user: {user_session}")
        history = list(
            collection.find({"user_session": user_session})
                      .sort("timestamp", -1)
                      .limit(limit)
        )

        # Convert ObjectId and datetime to string for JSON response
        for item in history:
            item["_id"] = str(item["_id"])
            item["timestamp"] = item["timestamp"].isoformat()

        client.close()
        print(f"✅ Fetched {len(history)} history records successfully.")
        return history

    except Exception as e:
        print(f"❌ Error fetching history from MongoDB: {e}")
        return []


# ==========================================================
# 🧪 Manual Test (Optional)
# ==========================================================
if __name__ == "__main__":
    print("🔍 Testing MongoDB connection and insert operation...")

    test_id = save_document_history(
        user_session="test_user",
        original_text="This is a sample original document.",
        simplified_text="This is a simplified version.",
        filename="sample.txt"
    )

    if test_id:
        print(f"✅ Test insert successful. Document ID: {test_id}")
    else:
        print("❌ Test insert failed.")

    # Fetch back recent entries
    print("📜 Fetching test user's history:")
    history = get_user_history("test_user", limit=3)
    for record in history:
        print(record)
