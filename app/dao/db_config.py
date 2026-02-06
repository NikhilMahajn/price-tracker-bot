from motor.motor_asyncio import AsyncIOMotorClient
from app.config import DATABASE_URL,DB_NAME

client = AsyncIOMotorClient(DATABASE_URL)
db = client[DB_NAME]

users_collection = db.users

