from sqlalchemy import Column,String,Integer,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Spot_Request(Base):
    __tablename__="spot_requests" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    status=Column(Boolean,default=False,nullable=False)

    #links spotter_request to a user
    spotter_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #links spotter_request to a user
    requester_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    # Need foreign_keys specified so SQLAlchemy knows which key to use
    user = relationship("User", foreign_keys=[spotter_id], backref="spotter_requests")
    peer = relationship("User", foreign_keys=[requester_id], backref="requester_requests")
