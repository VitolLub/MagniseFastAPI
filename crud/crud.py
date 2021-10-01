import os
import datetime
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException,Response,status
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import update
from pydantic import BaseModel
from models.users import Users
from models.users import Users as ModelUsers
from schemas.users import Users as SchemaUsers
from schemas.users import ChanegePass as SchemaChanegePass
import re
from models.users import Users

load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# Get full list of users
async def get_all_users():
    return db.session.query(Users).all()

#email validator
async def valid_email(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

# Create user rule
async def create_user(user):
    #check pass length
    if len(user.password)<5:
        raise HTTPException(status_code=406, detail="Pass have length less then 5 limbols")
    if not valid_email(user.email):
        raise HTTPException(status_code=406, detail="Email not valid ")
    else:
        db_user = ModelUsers(username=user.username, email=user.email, password=hashed_password)
        db.session.add(db_user)
        db.session.commit()
        return db_user


# update password rule
async def update_password(user_id,new):
    if len(new.new_password) < 5:
        return {'Error': 'Pass must have 5 simbols or more'}
    try:
        q = update(Users).where(Users.id == user_id).values(password=new.new_password)
        db.session.execute(q)
        db.session.commit()
        return HTTPException(
        status_code=200, detail="User created"
    )
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
# delete user rule
async def delete_user(user_id):
    entity = db.session.query(Users).filter(Users.id == user_id).first()
    try:
        db.session.delete(entity)
        db.session.commit()
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND)