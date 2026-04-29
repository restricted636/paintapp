from pydantic import BaseModel, Field
from typing import Optional


class ColorCreate(BaseModel):
    hex_code: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    rgb_r: int = Field(..., ge=0, le=255)
    rgb_g: int = Field(..., ge=0, le=255)
    rgb_b: int = Field(..., ge=0, le=255)
    cmyk_c: Optional[float] = Field(None, ge=0, le=100)
    cmyk_m: Optional[float] = Field(None, ge=0, le=100)
    cmyk_y: Optional[float] = Field(None, ge=0, le=100)
    cmyk_k: Optional[float] = Field(None, ge=0, le=100)
    lab_l: Optional[float] = Field(None, ge=0, le=100)
    lab_a: Optional[float] = Field(None, ge=-128, le=127)
    lab_b: Optional[float] = Field(None, ge=-128, le=127)
    h: Optional[float] = Field(None, ge=0, le=360)
    s: Optional[float] = Field(None, ge=0, le=100)
    l: Optional[float] = Field(None, ge=0, le=100)
    name: Optional[str] = Field(None, max_length=100)
    note: Optional[str] = Field(None, max_length=500)


class ColorResponse(BaseModel):
    id: int
    user_id: int
    hex_code: str
    rgb_r: int
    rgb_g: int
    rgb_b: int
    cmyk_c: Optional[float]
    cmyk_m: Optional[float]
    cmyk_y: Optional[float]
    cmyk_k: Optional[float]
    lab_l: Optional[float]
    lab_a: Optional[float]
    lab_b: Optional[float]
    h: Optional[float]
    s: Optional[float]
    l: Optional[float]
    name: Optional[str]
    note: Optional[str]
    created_at: int

    class Config:
        from_attributes = True