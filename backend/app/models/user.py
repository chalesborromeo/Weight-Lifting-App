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
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    clubs = relationship("Club", secondary=club_members, back_populates="members")
    owned_clubs = relationship('Club', back_populates="owner", foreign_keys="Club.owner_id", cascade="all, delete-orphan")
    prs = relationship("PR", back_populates="user", cascade="all, delete-orphan")
    body_metrics = relationship("BodyMetric", back_populates="user", cascade="all, delete-orphan")
    favorite_exercises = relationship("FavoriteExercise", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="reporter", foreign_keys="Report.reporter_id", cascade="all, delete-orphan")