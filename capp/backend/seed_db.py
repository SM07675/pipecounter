import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime
import random

load_dotenv()

# MongoDB configuration
MONGO_URL = os.getenv("MONGO_URL")

# Construct URL if not provided but auth vars are
if not MONGO_URL:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "27017")
    
    if DB_USER and DB_PASSWORD:
        # Assuming standard auth mechanism
        MONGO_URL = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    else:
        MONGO_URL = f"mongodb://{DB_HOST}:{DB_PORT}"

DB_NAME = os.getenv("DB_NAME", "capp_db")

async def seed_data():
    print(f"Connecting to {MONGO_URL}...")
    try:
        client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print("Connected to MongoDB.")
    except Exception as e:
        print(f"FAILED to connect: {e}")
        return

    print("Clearing existing data...")
    await db["predictions"].delete_many({})

    print("Inserting sample data...")
    sample_data = []
    classes = ["person", "car", "bus", "truck", "bicycle"]
    
    for i in range(10):
        details = {
            cls: random.randint(0, 5) 
            for cls in random.sample(classes, k=random.randint(2, 4))
        }
        total_count = sum(details.values())
        
        doc = {
            "filename": f"sample_image_{i}.jpg",
            "object_count": total_count,
            "details": details,
            "created_at": datetime.now().isoformat()
        }
        sample_data.append(doc)

    result = await db["predictions"].insert_many(sample_data)
    print(f"Successfully inserted {len(result.inserted_ids)} documents.")
    
    # Verify
    count = await db["predictions"].count_documents({})
    print(f"Total documents in collection: {count}")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(seed_data())
