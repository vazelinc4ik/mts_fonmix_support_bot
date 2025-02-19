from typing import List
from sqlalchemy import (
    ForeignKey,
    Integer,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .base import Base


class StaticInfo(Base):
    __tablename__ = "static_info"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    ip: Mapped[str] = mapped_column(String, nullable=False)
    mask: Mapped[str] = mapped_column(String, nullable=False)
    gateway: Mapped[str] = mapped_column(String, nullable=False)
    tv_id: Mapped[int] = mapped_column(Integer, ForeignKey("tv_details.id"), nullable=False)
    
    tv_detail: Mapped["TVDetails"] = relationship("TVDetails", back_populates="static_info") # type: ignore
    