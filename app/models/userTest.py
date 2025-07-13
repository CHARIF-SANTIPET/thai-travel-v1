from pydantic import BaseModel

class UserTest(BaseModel):
    username: str
    password: str