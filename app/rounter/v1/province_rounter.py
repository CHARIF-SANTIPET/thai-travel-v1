from fastapi import APIRouter, Depends, HTTPException , status

from sqlalchemy.orm import Session
from ...database import get_db
from ...models.province import Province
from ...schemas.province_schema import ProvinceCreate, ProvinceResponse
from ...auth.authentication import get_current_user
from decimal import Decimal

rounter = APIRouter(tags=["province"])

@rounter.post("/provinces/", response_model=ProvinceResponse)
def create_province(province: ProvinceCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    
    existing_province = db.query(Province).filter(Province.name == province.name).first()
    if existing_province:
        raise HTTPException(status_code=400, detail="Province already exists")
    
    db_province = Province(
        name=province.name,
        type=province.type,
        price=province.price
    )
    db.add(db_province)
    db.commit()
    db.refresh(db_province)
    return db_province

@rounter.get("/provinces/{province_id}", response_model=ProvinceResponse)
def get_province(province_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    
    db_province = db.query(Province).filter(Province.id == province_id).first()
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    return db_province

@rounter.get("/provinces/", response_model=list[ProvinceResponse])
def get_provinces(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    
    provinces = db.query(Province).offset(skip).limit(limit).all()
    return provinces

@rounter.put("/provinces/{province_id}", response_model=ProvinceResponse)
def update_province(province_id: int, province: ProvinceCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    
    db_province = db.query(Province).filter(Province.id == province_id).first()
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    
    db_province.name = province.name
    db_province.type = province.type
    db_province.price = Decimal(province.price)
    db.commit()
    db.refresh(db_province)
    return db_province

@rounter.delete("/provinces/{province_id}", response_model=ProvinceResponse)
def delete_province(province_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    
    db_province = db.query(Province).filter(Province.id == province_id).first()
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    
    db.delete(db_province)
    db.commit()
    return db_province

