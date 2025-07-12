from fastapi import APIRouter
from . import v1

rounter = APIRouter()
rounter.include_router(v1.rounter)