from sqlalchemy import Column,Integer,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Spot_Request(Base):
    __tablename__="spot_requests" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    status=Column(Boolean,default=False,nullable=False)

    #links spot_request to users
    spotter_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    requester_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    # Eager-loaded so API responses can serialize without re-querying.
    spotter = relationship("User", foreign_keys=[spotter_id], backref="spotter_requests", lazy="joined")
    requester = relationship("User", foreign_keys=[requester_id], backref="requester_requests", lazy="joined")
