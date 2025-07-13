from ..database import Base
from sqlalchemy import Column, Integer, String, Enum, Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship


from ..schemas.province_schema import ProvinceType

class Province(Base):
    __tablename__ = "provinces"

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(Enum(ProvinceType), index=True)
    price = Column(Numeric(10, 2))
    
    bookings = relationship("Booking", back_populates="province")