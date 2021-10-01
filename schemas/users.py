from pydantic import BaseModel, EmailStr


class Users(BaseModel):
    username: str
    email: str
    password: str
    class Config:
        orm_mode = True

class ChanegePass(BaseModel):
    new_password:str
