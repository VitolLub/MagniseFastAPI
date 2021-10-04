import os
import datetime
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException,Response,status

from sqlalchemy import update
from pydantic import BaseModel
from models.users import Users as ModelUsers
from schemas.users import Users as SchemaUsers
from schemas.users import ChanegePass as SchemaChanegePass
import re
from models.users import Users
import bcrypt
import asyncio
from sqlalchemy.orm import Session  # type: ignore



# Get full list of users
def get_all_users(session: Session):
    return session.query(Users).all()


# email validator
def valid_email(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


# Create user rule
def create_user(session,user):
    #check pass length
    if len(user.password)<5:
        raise HTTPException(status_code=406, detail="Pass have length less then 5 limbols")
    if not valid_email:
        raise HTTPException(status_code=406, detail="Email is not valid")
    else:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        db_user = ModelUsers(username=user.username, email=user.email, password=hashed_password)
        session.add(db_user)
        session.commit()
        return db_user


# update password rule
def update_password(session,user_id,new):
    if len(new.new_password) < 5:
        return {'Error': 'Pass must have 5 simbols or more'}
    try:
        hashed_password = bcrypt.hashpw(new.new_password.encode('utf-8'), bcrypt.gensalt())
        q = update(Users).where(Users.id == user_id).values(password=hashed_password)
        session.execute(q)
        session.commit()
        return HTTPException(
        status_code=200, detail="Password updated"
    )
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
# delete user rule
def delete_user(session,user_id):
    entity = session.query(Users).filter(Users.id == user_id).first()
    try:
        session.delete(entity)
        session.commit()
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
