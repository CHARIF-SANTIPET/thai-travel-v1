from ..database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship

def get_thai_time():
    return datetime.now(ZoneInfo("Asia/Bangkok"))

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    address = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, index=True)  # e.g., "user", "admin"

    created_at = Column(DateTime(timezone=True), default=get_thai_time)
    updated_at = Column(DateTime(timezone=True), default=get_thai_time, onupdate=get_thai_time)

    user_bookings : Mapped[list["Booking"]] = relationship("Booking", back_populates="user")
