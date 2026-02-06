from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from bson import ObjectId


# =========================
# ObjectId helper
# =========================
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")



# =========================
# USERS
# =========================
class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    plan: Literal["free", "premium"] = "free"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        

# =========================
# Procut
# =========================
class Product(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    platform: Literal["amazon", "flipkart"]
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    