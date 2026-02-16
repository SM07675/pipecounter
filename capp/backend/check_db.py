import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import sys

# Add current directory to path so we can import if needed, though we rely on installed packages
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

async def ping_server():
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    print(f"Attempting to connect to: {mongo_url}")
    try:
        import certifi
        # Set a short timeout for the test
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
        # The is_master command is cheap and checks connectivity
        await client.admin.command('ping')
        print("SUCCESS: Connected to MongoDB!")
    except Exception as e:
        print(f"FAILURE: Could not connect to MongoDB. Error: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        asyncio.run(ping_server())
    except ImportError:
        print("Error: 'motor' module not found. Please run 'pip install -r requirements.txt'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
