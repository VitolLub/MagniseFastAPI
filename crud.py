import os
import datetime
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException,Response,status
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import update
from pydantic import BaseModel
from models import Users
from models import Users as ModelUsers
from schema import Users as SchemaUsers
from schema import ChanegePass as SchemaChanegePass
import re
from models import Users

class UserCRUD():

    # Get full list of users
    def get_all_users(self):
        return db.session.query(Users).all()

    #email validator
    def valid_email(self,email):
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

    # Create user rule
    def create_user(self, user):
        #check pass length
        if len(user.password)<5:
            return {'Error':'Pass must have 5 simbols or more'}
        if self.valid_email(self, user.email)==False:
            return {'Error': 'Email not valid'}
        else:
            date_time = datetime.datetime.now()
            db_user = ModelUsers(username=user.username, email=user.email, password=user.password, register_date=date_time)
            db.session.add(db_user)
            db.session.commit()
            return db_user
    # update password rule
    def update_password(self,user_id,new):
        try:
            q = update(Users).where(Users.id == user_id).values(password=new.new_password)
            db.session.execute(q)
            db.session.commit()
            return {'ok': user_id}
        except:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
    # delete user rule
    def delete_user(self,user_id):
        entity = db.session.query(Users).filter(Users.id == user_id).first()
        try:
            db.session.delete(entity)
            db.session.commit()
        except:
            return Response(status_code=status.HTTP_404_NOT_FOUND)