from fastapi import FastAPI

from . import rounter



app = FastAPI()

app.include_router(rounter.rounter)
