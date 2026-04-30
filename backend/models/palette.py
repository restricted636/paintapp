from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from models import Base
from models.palette_color import palette_colors


class Palette(Base):
    __tablename__ = "palettes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)
    tags = Column(JSON, nullable=True)  # Store as JSON array
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationship with User
    user = relationship("User", back_populates="palettes")
    
    # Relationship with Color (many-to-many via palette_colors)
    colors = relationship("Color", secondary=palette_colors, back_populates="palettes")