from sqlalchemy import Column,String,Integer,ForeignKey,Table
from sqlalchemy.orm import relationship
from app.db.base import Base

club_members=Table(
    "club_members",
    Base.metadata,
    Column("club_id",ForeignKey("clubs.id")),
    Column("user_id",ForeignKey("users.id"))
)
class Club(Base):
    __tablename__="clubs" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    privacy=Column(String(100),nullable=False)

    #lets you do club.post
    posts=relationship("Post",back_populates="club")

    members=relationship("User",secondary=club_members)