from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime,timezone

class Comment(Base):
    __tablename__="comments" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    text=Column(String(100),nullable=False)
    date=Column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)

    #links comment to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #links comment to a post
    post_id=Column(Integer,ForeignKey("posts.id"),nullable=False)

    #lets you do comments.user in python
    user=relationship("User",back_populates="comments")

    #lets you do comments.post
    post=relationship("Post",back_populates="comments")
