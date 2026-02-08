from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema



# =========================
# ObjectId helper
# =========================
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler: GetCoreSchemaHandler
    ):
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.no_info_plain_validator_function(
                cls.validate
            ),
        )

    @classmethod
    def validate(cls, value):
        if isinstance(value, ObjectId):
            return value
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema, handler: GetJsonSchemaHandler
    ):
        schema.update(type="string")
        return schema


# =========================
# USERS
# =========================

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    plan: Literal["free", "premium"] = "free"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            PyObjectId: str
        }
    }
        

# =========================
# Prodcut
# =========================
class Product(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    platform: Literal["amazon", "flipkart"]
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            PyObjectId: str
        }
    }


# =========================
# USER ↔ PRODUCT TRACKING
# =========================
class UserProductModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId
    product_id: PyObjectId
    initial_price: int
    target_price: Optional[int] = None
    is_tracking: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            PyObjectId: str
        }
    }


# =========================
# PRICE HISTORY
# =========================
class PriceHistoryModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    product_id: PyObjectId
    price: int
    checked_at: datetime = Field(default_factory=datetime.utcnow)

    
    model_config = {
        "populate_by_name": True,
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            PyObjectId: str
        }
    }
