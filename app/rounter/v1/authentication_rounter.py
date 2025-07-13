from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ...auth.authentication import oauth2_scheme, get_current_user, create_access_token
from ...models.userTest import UserTest
from ...models.user import User
from ...data.user import users_db
from ...database import get_db 
from sqlalchemy.orm import Session

rounter = APIRouter(tags=["authentication"])

@rounter.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None or user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
    

@rounter.get("/protected")
async def protected_route(username: dict = Depends(get_current_user)):
    return {"message": f"Hello, {username['username']}! Your role is {username['role']}. This is a protected resource."}