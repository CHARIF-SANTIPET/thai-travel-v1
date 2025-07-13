from pydantic import BaseModel, Field, model_validator, root_validator
from ..schemas.province_schema import ProvinceResponse

from datetime import date
from typing import Optional
import decimal

from enum import Enum

class BookingStatus(str, Enum):
    confirmed = "confirmed"
    in_use = "in_use"
    cancelled = "cancelled"

class BookingBase(BaseModel):
    user_id: int = Field(..., gt=0)
    province_id: int = Field(..., gt=0)
    # booking_price: decimal.Decimal = Field(..., gt=0, description="Booking price in THB")
    checkin_date: date
    checkout_date: date
    status: BookingStatus = Field(default=BookingStatus.confirmed, description="Booking status")

    @model_validator(mode="after")
    def check_dates(self):
        if self.checkout_date <= self.checkin_date:
            raise ValueError("checkout_date ต้องอยู่หลัง checkin_date")
        return self


class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    booking_price: decimal.Decimal = Field(..., gt=0, description="Booking price in THB")

    class Config:
        from_attributes = True

class BookingWithProvince(BookingResponse):
    province: ProvinceResponse

    class Config:
        from_attributes = True


