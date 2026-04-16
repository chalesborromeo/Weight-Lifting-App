from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
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

    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)

    #relationships
    club = relationship("Club", back_populates="posts")
    user=relationship("User",back_populates="posts")
    comments=relationship("Comment", back_populates="post")

