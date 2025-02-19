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
from .tv_details import TVDetails

class Stores(Base):
    __tablename__ = "stores"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.id"), nullable=False)
    
    region: Mapped["Regions"] = relationship("Regions", back_populates="stores") # type: ignore
    dns: Mapped[List["DNSTable"]] = relationship( # type: ignore
        "DNSTable",
        secondary="regions",
        primaryjoin="Stores.region_id == Regions.id",
        secondaryjoin="Regions.id == DNSTable.region_id",
        viewonly=True,
        lazy="joined"
    )
    tv_details: Mapped[List["TVDetails"]] = relationship("TVDetails", back_populates="store_info", lazy="joined")

    
    