from pydantic import BaseModel
from typing import Optional

class GameBase(BaseModel):
    title: str
    price: float
    provider_id: int

class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: int
    is_published: bool

    class Config:
        from_attributes = True

class ProviderCreate(BaseModel):
    name: str
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Epic Games",
                "email": "support@epicgames.com"
            }
        }
    
class ProviderRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True  # для SQLAlchemy