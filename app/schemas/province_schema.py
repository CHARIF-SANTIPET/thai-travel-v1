from pydantic import BaseModel
import decimal

from enum import Enum

class ProvinceType(str, Enum):
    capital = "capital"
    secondary = "secondary"

class ProvinceBase(BaseModel):
    name: str
    type: ProvinceType  
    price : decimal.Decimal = 0.0
    
class ProvinceCreate(ProvinceBase):
    pass

class ProvinceResponse(ProvinceBase):
    id: int

    class Config:
        from_attributes = True
