from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime,timezone

class Post(Base):
    __tablename__="posts" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    date=Column(DateTime,default=lambda: datetime.now(timezone.utc),nullable=False)
    text=Column(String(100),nullable=True)
    likes=Column(Integer,default=0,nullable=False)

    #links post to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #links post to a workout
    workout_id=Column(Integer,ForeignKey("workouts.id"),nullable=True)

    #lets you do posts.user in python
    user=relationship("User",back_populates="posts")

