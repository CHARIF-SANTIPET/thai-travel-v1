from fastapi import APIRouter, Depends, HTTPException , status

from sqlalchemy.orm import Session

from ...database import get_db , Base, engine
from ...models.user import User
from ...schemas.user_schema import UserCreate, UserResponse

rounter = APIRouter(tags=["user"])

@rounter.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()

    if existing_user:
        # ตรวจสอบว่าอะไรซ้ำ
        detail = "Username or email already taken."
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
        )
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        phone=user.phone,
        email=user.email,
        password=user.password,  # Ensure to hash the password in a real application
        role=user.role  # Add role field
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@rounter.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
@rounter.get("/users/", response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@rounter.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()

    if existing_user:
        # ตรวจสอบว่าอะไรซ้ำ
        detail = "Username or email already taken."
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
        )
    
    db_user.username = user.username
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.address = user.address
    db_user.phone = user.phone
    db_user.email = user.email
    db_user.password = user.password
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user

@rounter.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
