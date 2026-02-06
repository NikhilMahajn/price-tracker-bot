from datetime import datetime
from app.dao.db_config import users_collection
from app.dao.schemas import UserCreate

async def create_user(user: UserCreate):
    existing = await users_collection.find_one(
        {"telegram_id": user.telegram_id}
    )

    if existing:
        return {"message": "User already exists"}

    await users_collection.insert_one({
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "created_at": datetime.utcnow(),
        "is_active": True
    })

    return {"status": 200, "message": "User created"}
