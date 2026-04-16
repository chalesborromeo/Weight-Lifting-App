from sqlalchemy import Column,String,Integer,ForeignKey,Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Workout(Base):
    __tablename__="workouts" #name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #Fields
    name=Column(String(100),nullable=False)
    type=Column(String(100),nullable=True)
    duration=Column(Float,nullable=True)

    #links workout to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #lets you do workout.user in Python
    user=relationship("User",back_populates="workouts")