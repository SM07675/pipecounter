import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def test_crud():
    mongo_url = os.getenv("MONGO_URL")
    db_name = os.getenv("DB_NAME", "capp_db")
    
    if not mongo_url:
        print("Error: MONGO_URL not found in .env")
        return

    print(f"Connecting to {db_name}...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # 1. Insert
    test_doc = {"_id": "test_connection_id", "status": "all_good", "timestamp": "now"}
    try:
        await db.test_collection.insert_one(test_doc)
        print("PASS: Insert command successful")
    except Exception as e:
        if "E11000" in str(e):
             print("INFO: Test document already exists (that's fine)")
        else:
             print(f"FAIL: Insert failed: {e}")
             return

    # 2. Read
    doc = await db.test_collection.find_one({"_id": "test_connection_id"})
    if doc:
        print(f"PASS: Read command successful: {doc['status']}")
    else:
        print("FAIL: Read failed: Document not found")

    # 3. Delete
    result = await db.test_collection.delete_one({"_id": "test_connection_id"})
    if result.deleted_count > 0:
        print("PASS: Delete command successful")
    else:
        print("WARN: Delete warning: No document deleted")

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_crud())
