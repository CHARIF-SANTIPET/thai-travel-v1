from fastapi import APIRouter
from . import authentication_rounter, user_rounter

rounter = APIRouter(prefix="/v1")
rounter.include_router(authentication_rounter.rounter)
rounter.include_router(user_rounter.rounter)