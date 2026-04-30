from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, ForeignKey, Table
from models import Base


# Association table for many-to-many relationship between Palette and Color
palette_colors = Table(
    "palette_colors",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("palette_id", Integer, ForeignKey("palettes.id"), nullable=False, index=True),
    Column("color_id", Integer, ForeignKey("colors.id"), nullable=False, index=True),
    Column("ratio", Float, nullable=False, default=1.0),  # Color ratio in palette (0-1)
)