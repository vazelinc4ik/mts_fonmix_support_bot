from typing import List
from sqlalchemy import (
    Integer,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .base import Base


class Regions(Base):
    __tablename__ = "regions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    stores: Mapped[List["Stores"]] = relationship("Stores", back_populates="region") #type: ignore
    dns_records: Mapped[List["DNSTable"]] = relationship("DNSTable", back_populates="region") #type: ignore