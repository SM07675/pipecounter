from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "capp_db")

import certifi

try:
    client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where(), tlsAllowInvalidCertificates=True)
    db = client[DB_NAME]
    display_url = MONGO_URL.split("@")[-1] if "@" in MONGO_URL else MONGO_URL
    print(f"Connected to MongoDB at ...@{display_url}, database: {DB_NAME}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    client = None
    db = None
