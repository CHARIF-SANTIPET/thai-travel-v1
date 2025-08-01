from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    address: str = Field(..., min_length=5, max_length=100)
    phone: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$")  # E.164 format
    email: EmailStr 
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(..., min_length=3, max_length=20)  # e.g., "user", "admin"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# class UserWithBookings(UserResponse):
#     bookings: list["booking"] = []  

#     class Config:
#         orm_mode = True
