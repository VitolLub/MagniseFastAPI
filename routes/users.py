import os
import datetime
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException,Response,status,APIRouter,Depends
from schemas.users import Users as SchemaUsers
from schemas.users import Users as ModelUsers
from schemas.users import ChanegePass as SchemaChanegePass
import crud.crud
import asyncio
from models.users import Users
import bcrypt
from models.database import SessionLocal, engine
from sqlalchemy.orm import Session  # type: ignore

users = APIRouter()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


#root page enpoint
@users.get("/")
async def root():
    return {"message": "Test Message"}
# get full user list enpoint
@users.get("/get-user-list")
async def get_user_list(session: Session = Depends(get_session)):
    return crud.crud.get_all_users(session)

# create user enpoint
@users.post("/create-user/", response_model=SchemaUsers)
async def create_user(user: SchemaUsers,session: Session = Depends(get_session)):
    return crud.crud.create_user(session,user)


# remve user by id enpoint
@users.delete("/delete-user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int,session: Session = Depends(get_session)):
    result = crud.crud.delete_user(session,user_id)
    return result

#update password enpoint
@users.put("/update-password/{user_id}",response_model=SchemaChanegePass)
async def update_password(user_id:int,new: SchemaChanegePass,session: Session = Depends(get_session)):
    result = crud.crud.update_password(session,user_id,new)
    return result
