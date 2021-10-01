import os
import datetime
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException,Response,status,APIRouter
from schemas.users import Users as SchemaUsers
from schemas.users import ChanegePass as SchemaChanegePass
import crud.crud
load_dotenv(".env")
users = APIRouter()


#root page enpoint
@users.get("/")
async def root():
    return {"message": "Test Message"}
# remve user by id enpoint
@users.delete("/delete-user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int):
    result = crud.crud.delete_user(user_id)
    return result

#update password enpoint
@users.put("/update-password/{user_id}",response_model=SchemaChanegePass)
async def update_password(user_id:int,new: SchemaChanegePass):
    result = crud.crud.update_password(user_id,new)
    return result

# create user enpoint
@users.post("/create-user/", response_model=SchemaUsers)
async def create_user(user: SchemaUsers):
    result = crud.crud.create_user(user)
    return result

# get full user list enpoint
@users.get("/get-user-list")
def get_user_list():
    users = crud.crud.get_all_users()
    return users


#
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
