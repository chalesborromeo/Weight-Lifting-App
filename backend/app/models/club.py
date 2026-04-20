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
    name=Column(String(100), nullable=False)
    privacy=Column(String(100),nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    #relationships
    owner=relationship("User",foreign_keys=[owner_id], back_populates="owned_clubs")
    posts=relationship("Post",back_populates="club", cascade="all, delete-orphan")
    members=relationship("User",secondary=club_members, back_populates="clubs")