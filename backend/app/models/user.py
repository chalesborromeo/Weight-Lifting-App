from sqlalchemy import Column,String,Integer
from app.core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #auth fields
    email=Column(String(100),nullable=False,unique=True)
    password=Column(String(100),nullable=False)
    
     # RELATIONSHIPS
    profile = relationship("Profile", back_populates="user", uselist=False)
    workouts = relationship("Workout", back_populates="user")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    notifications = relationship("Notification", back_populates="user")