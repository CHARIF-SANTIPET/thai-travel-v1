from ..database import Base
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List
from sqlalchemy import Column, Integer, String, Enum, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from ..schemas.booking_schema import BookingStatus


def get_thai_time():
    return datetime.now(ZoneInfo("Asia/Bangkok"))

class Booking(Base):
    __tablename__ = "bookings"

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    province_id : Mapped[int] = mapped_column(ForeignKey("provinces.id"))
    booking_price = Column(Numeric(10, 2), nullable=False)
    checkin_date = Column(String, nullable=False) 
    checkout_date = Column(String, nullable=False) 
    status = Column(Enum(BookingStatus), default=BookingStatus.confirmed, index=True)

    created_at = Column(DateTime(timezone=True), default=get_thai_time)
    updated_at = Column(DateTime(timezone=True), default=get_thai_time, onupdate=get_thai_time)

    user = relationship("User", back_populates="user_bookings")
    province = relationship("Province", back_populates="bookings")