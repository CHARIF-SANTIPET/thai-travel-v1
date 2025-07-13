# from pydantic import BaseModel, Field, root_validator
# from .schemas.user_schema import UserResponse

# from datetime import date
# from typing import Optional
# import decimal


# class BookingBase(BaseModel):
#     user_id: int = Field(..., gt=0)
#     province_id: int = Field(..., gt=0)
#     accommodation_id: int = Optional(gt=0, default=None)
#     booking_price: decimal.Decimal = Field(..., gt=0, description="Booking price in THB")
#     checkin_date: date
#     checkout_date: date
#     status: str = Field(..., min_length=3, max_length=20)

#     @root_validator
#     def check_dates(cls, values):
#         checkin = values.get("checkin_date")
#         checkout = values.get("checkout_date")
#         if checkin and checkout and checkout <= checkin:
#             raise ValueError("checkout_date ต้องอยู่หลัง checkin_date")
#         return values


# class BookingCreate(BookingBase):
    
#     pass

# class BookingResponse(BookingBase):
#     id: int

#     class Config:
#         orm_mode = True

# class BookingWithUser(BookingResponse):
#     user: UserResponse

#     class Config:
#         orm_mode = True