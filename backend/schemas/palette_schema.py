from pydantic import BaseModel, Field
from typing import Optional


class PaletteCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_public: bool = False
    tags: Optional[list[str]] = None


class PaletteUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_public: Optional[bool] = None
    tags: Optional[list[str]] = None


class PaletteResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str]
    is_public: bool
    tags: Optional[list[str]]
    created_at: str

    class Config:
        from_attributes = True