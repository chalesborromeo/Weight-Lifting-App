from sqlalchemy import Column,String,Integer,Boolean,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime,timezone

class Report(Base):
    __tablename__="reports" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    reason=Column(String(500),nullable=False)
    created_at=Column(DateTime,default=lambda: datetime.now(timezone.utc),nullable=False)
    resolved=Column(Boolean,default=False,nullable=False)

    #links report to reporter and reported post
    reporter_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    post_id=Column(Integer,ForeignKey("posts.id"),nullable=False)

    #relationships
    reporter=relationship("User",back_populates="reports")
    post=relationship("Post",back_populates="reports")
