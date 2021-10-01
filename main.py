from fastapi import FastAPI
from routes.users import users
from fastapi_sqlalchemy import DBSessionMiddleware, db
import os

app = FastAPI(
    title="Users API",
    description="a REST API using python and mysql",
    version="0.0.1"
)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.include_router(users)