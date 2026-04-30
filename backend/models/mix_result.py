from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models import Base


class MixResult(Base):
    __tablename__ = "mix_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    palette_id = Column(Integer, ForeignKey("palettes.id"), nullable=False, index=True)
    result_color_id = Column(Integer, ForeignKey("colors.id"), nullable=False, index=True)
    target_color_id = Column(Integer, ForeignKey("colors.id"), nullable=False, index=True)
    accuracy = Column(Float, nullable=False)  # 0-100 percentage
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    palette = relationship("Palette", backref="mix_results")
    result_color = relationship("Color", foreign_keys=[result_color_id], backref="mix_results_as_result")
    target_color = relationship("Color", foreign_keys=[target_color_id], backref="mix_results_as_target")