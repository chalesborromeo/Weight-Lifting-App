from sqlalchemy import Column,String,Integer
from app.db.base import Base
from sqlalchemy.orm import relationship
from app.models.club import club_members

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
    clubs = relationship("Club", secondary=club_members, back_populates="members")
    owned_clubs = relationship('Club', back_populates="owner", foreign_keys="Club.owner_id")