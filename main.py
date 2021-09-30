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
from crud import UserCRUD
load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])



@app.get("/")
async def root():
    return {"message": "Test Message"}

@app.delete("/delete-user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int):
    result = UserCRUD.delete_user(user_id)
    return result

#update password
@app.put("/update-password/{user_id}",response_model=SchemaChanegePass)
async def update_password(user_id:int,new: SchemaChanegePass):
    result = UserCRUD.update_password(user_id,new)
    return result

@app.post("/create-user/", response_model=SchemaUsers)
def create_user(user: SchemaUsers):
    result = UserCRUD.create_user(user)
    return result

@app.get("/get-user-list/")
def get_user_list():
    users = UserCRUD.get_all_users()
    return users




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
