from sqlalchemy import Column,String,Integer,Float,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Profile(Base):
    __tablename__="profiles" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #Fields
    name=Column(String(100),nullable=False)
    age=Column(Integer,nullable=False)
    gym=Column(String(100),nullable=False)
    bio=Column(String(100),nullable=True)
    weight=Column(Float,nullable=True)
    location=Column(String(100),nullable=True)

    #links profile to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #lets you do profile.user in python
    user=relationship("User",back_populates="profile")



