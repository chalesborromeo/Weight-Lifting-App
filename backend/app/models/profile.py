from sqlalchemy import Column,String,Integer,Float,ForeignKey,Date
from sqlalchemy.orm import relationship
from app.db.base import Base

class Profile(Base):
    __tablename__="profiles" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #Identity
    first_name=Column(String(50),nullable=True)
    last_name=Column(String(50),nullable=True)
    name=Column(String(100),nullable=True)  # legacy single-name field; superseded by first_name/last_name
    profile_picture_url=Column(String(500),nullable=True)

    #Bio
    bio=Column(String(500),nullable=True)
    primary_sport=Column(String(50),nullable=True)

    #Location
    location=Column(String(100),nullable=True)  # city
    state=Column(String(50),nullable=True)
    gym=Column(String(100),nullable=True)  # legacy gym name string

    #Athlete info
    birthdate=Column(Date,nullable=True)
    age=Column(Integer,nullable=True)  # legacy; prefer birthdate
    gender=Column(String(20),nullable=True)
    weight=Column(Float,nullable=True)
    goal_weight=Column(Float,nullable=True)

    #links profile to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #set_gym: FK to the structured Gym entity (nullable during transition from string `gym` field)
    gym_id=Column(Integer,ForeignKey("gyms.id"),nullable=True)

    #lets you do profile.user in python
    user=relationship("User",back_populates="profile")
    set_gym=relationship("Gym",back_populates="profiles")
