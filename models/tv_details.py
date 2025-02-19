
from sqlalchemy import (
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import(
    Mapped,
    mapped_column,
    relationship
)

from .base import Base

class TVDetails(Base):
    __tablename__ = "tv_details"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    store_id: Mapped[int] = mapped_column(Integer, ForeignKey("stores.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    point_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    store_info: Mapped["Stores"] = relationship("Stores", back_populates="tv_details") #type: ignore
    static_info: Mapped["StaticInfo"] = relationship("StaticInfo", back_populates="tv_detail", lazy="joined") #type: ignore
    