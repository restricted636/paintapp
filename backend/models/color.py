from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
from models.palette_color import palette_colors


class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    hex_code = Column(String(7), nullable=False)  # e.g., "#FF5733"
    rgb_r = Column(Integer, nullable=False)  # 0-255
    rgb_g = Column(Integer, nullable=False)  # 0-255
    rgb_b = Column(Integer, nullable=False)  # 0-255
    cmyk_c = Column(Float, nullable=True)  # 0-100
    cmyk_m = Column(Float, nullable=True)  # 0-100
    cmyk_y = Column(Float, nullable=True)  # 0-100
    cmyk_k = Column(Float, nullable=True)  # 0-100
    lab_l = Column(Float, nullable=True)  # 0-100
    lab_a = Column(Float, nullable=True)  # -128 to 127
    lab_b = Column(Float, nullable=True)  # -128 to 127
    h = Column(Float, nullable=True)  # 0-360 (hue)
    s = Column(Float, nullable=True)  # 0-100 (saturation)
    l = Column(Float, nullable=True)  # 0-100 (lightness)
    name = Column(String(100), nullable=True)
    note = Column(String(500), nullable=True)
    created_at = Column(Integer, default=lambda: int(datetime.now(timezone.utc).timestamp()), nullable=False)

    # Relationship with User
    user = relationship("User", back_populates="colors")
    
    # Relationship with Palette (many-to-many via palette_colors)
    palettes = relationship("Palette", secondary=palette_colors, back_populates="colors")