from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime,timezone

class Peer(Base):
    __tablename__="peers" #Name of table in PostgreSQL

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    status=Column(String(100),nullable=False)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)

    #links peer to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #links peer to a peer
    peer_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    # Need foreign_keys specified so SQLAlchemy knows which key to use
    user = relationship("User", foreign_keys=[user_id], backref="my_peers")
    peer = relationship("User", foreign_keys=[peer_id], backref="their_peers")