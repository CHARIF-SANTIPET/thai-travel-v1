from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException , status

from sqlalchemy.orm import Session
from ...database import get_db
from ...models.booking import Booking
from ...models.user import User
from ...models.province import Province
from ...schemas.booking_schema import BookingCreate, BookingResponse, BookingWithProvince
from ...auth.authentication import get_current_user

rounter = APIRouter(tags=["booking"])


@rounter.post("/bookings/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    province: Province = db.query(Province).filter(Province.id == booking.province_id).first()
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    
    if province.type == "capital":
        price_result = province.price * Decimal("0.9")
    else :
        price_result = province.price * Decimal("0.8")
    

    user_obj : User = db.query(User).filter(User.username == current_user["username"]).first()

    if user_obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_booking = Booking(
        user_id=user_obj.id,
        province_id=booking.province_id,
        booking_price= price_result ,
        checkin_date=booking.checkin_date,
        checkout_date=booking.checkout_date,
        status=booking.status
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@rounter.get("/bookings/me", response_model=list[BookingResponse])
def get_my_bookings(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_obj : User = db.query(User).filter(User.username == current_user["username"]).first()
    bookings = db.query(Booking).filter(Booking.user_id == user_obj.id).all()
    return bookings

@rounter.put("/booking/me/{booking_id}", response_model=BookingResponse)
def update_my_booking(booking_id: int, booking: BookingCreate,db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_obj : User = db.query(User).filter(User.username == current_user["username"]).first()
    db_booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user_obj.id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db_booking.status = booking.status
    return db_booking

@rounter.get("/bookings/admin/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    user_obj : User = db.query(User).filter(User.username == current_user["username"]).first()
    db_booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user_obj.id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@rounter.get("/bookings/admin", response_model=list[BookingResponse])
def get_user_bookings(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    user_obj : User = db.query(User).filter(User.username == current_user["username"]).first()
    db_bookings = db.query(Booking).filter(Booking.user_id == user_obj.id).all()
    return db_bookings

@rounter.put("/bookings/admin/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    user_obj : User = db.query(User).filter(User.username == current_user["username"]).first()
    db_booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user_obj.id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db_booking.province_id = booking.province_id
    db_booking.booking_price = booking.booking_price
    db_booking.checkin_date = booking.checkin_date
    db_booking.checkout_date = booking.checkout_date
    db_booking.status = booking.status
    
    db.commit()
    db.refresh(db_booking)
    return db_booking

@rounter.delete("/bookings/admin/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    user_obj : User = db.query(User).filter(User.username == current_user["username"]).first()
    db_booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user_obj.id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(db_booking)
    db.commit()
    return {"detail": "Booking deleted successfully"}