from sqlalchemy import Column,Integer,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime,timezone

class BodyMetric(Base):
    __tablename__="body_metrics" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    weight=Column(Float,nullable=False)
    height=Column(Float,nullable=True)
    body_fat_pct=Column(Float,nullable=True)
    date=Column(DateTime,default=lambda: datetime.now(timezone.utc),nullable=False)

    #links metric to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #lets you do metric.user in python
    user=relationship("User",back_populates="body_metrics")
