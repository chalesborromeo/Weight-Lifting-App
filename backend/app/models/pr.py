from sqlalchemy import Column,String,Integer,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime,timezone

class PR(Base):
    __tablename__="prs" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    exercise_name=Column(String(100),nullable=False)
    weight=Column(Float,nullable=False)
    reps=Column(Integer,nullable=False)
    date=Column(DateTime,default=lambda: datetime.now(timezone.utc),nullable=False)

    #links pr to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #lets you do pr.user in python (eager-loaded so leaderboard responses can serialize without re-querying)
    user=relationship("User",back_populates="prs",lazy="joined")
