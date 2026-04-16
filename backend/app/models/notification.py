from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime,timezone

class Notification(Base):
    __tablename__="notifications" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    message=Column(String(100),nullable=False)
    type=Column(String(100),nullable=False)
    time=Column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)
    read=Column(Boolean,default=False,nullable=False)

    #links notification to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #lets you do notifications.user in python
    user=relationship("User",back_populates="notifications")
