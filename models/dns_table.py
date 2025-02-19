

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


class DNSTable(Base):
    __tablename__ = "dns_table"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.id"), nullable=False)
    
    region: Mapped["Regions"] = relationship("Regions", back_populates="dns_records") #type: ignore
    