from sqlalchemy import Column,String,Integer,Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Gym(Base):
    __tablename__="gyms" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    name=Column(String(100),nullable=False)
    address=Column(String(200),nullable=True)
    latitude=Column(Float,nullable=False)
    longitude=Column(Float,nullable=False)
    hours_open=Column(String(10),nullable=True)
    hours_close=Column(String(10),nullable=True)
    rating=Column(Float,nullable=True)

    #reverse relationship: profiles whose set_gym is this gym
    profiles=relationship("Profile",back_populates="set_gym")
