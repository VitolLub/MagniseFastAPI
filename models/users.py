from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()




class Users(Base):
    """
       The User model
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String,nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    register_date = Column(DateTime(timezone=True), server_default=func.now())
    password = Column(String, nullable=False)

