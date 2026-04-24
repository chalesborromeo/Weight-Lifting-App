from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.db.postgresql.factory import PostgreSQLFactory
from app.db.postgresql.connection import PostgreSQLConnection
from sqlalchemy import select
from app.models.peer import Peer
from pydantic import BaseModel


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


class PeerCreate(BaseModel):
    user_id: int
    peer_id: int
    status: str = "pending"


class PeerResponse(BaseModel):
    id: int
    status: str
    user_id: int
    peer_id: int

    model_config = {"from_attributes": True}


class PeersRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/peers", tags=["peers"])
        self.router.add_api_route("/", self.add_peer, methods=["POST"], response_model=PeerResponse)
        self.router.add_api_route("/user/{user_id}", self.get_peers, methods=["GET"], response_model=List[PeerResponse])
        self.router.add_api_route("/{peer_id}", self.get_peer, methods=["GET"], response_model=PeerResponse)
        self.router.add_api_route("/{peer_id}", self.remove_peer, methods=["DELETE"], response_model=PeerResponse)

    async def add_peer(self, peer_data: PeerCreate, session=Depends(get_db)):
        """Add a peer connection"""
        new_peer = Peer(
            user_id=peer_data.user_id,
            peer_id=peer_data.peer_id,
            status=peer_data.status
        )
        session.add(new_peer)
        session.commit()
        session.refresh(new_peer)
        return PeerResponse.model_validate(new_peer)

    async def get_peers(self, user_id: int, session=Depends(get_db)):
        """Get all peers for a user"""
        stmt = select(Peer).where(Peer.user_id == user_id)
        peers = session.execute(stmt).scalars().all()
        return [PeerResponse.model_validate(p) for p in peers]

    async def get_peer(self, peer_id: int, session=Depends(get_db)):
        """Get a specific peer connection"""
        stmt = select(Peer).where(Peer.id == peer_id)
        peer = session.execute(stmt).scalars().first()
        if not peer:
            raise HTTPException(status_code=404, detail="Peer not found")
        return PeerResponse.model_validate(peer)

    async def remove_peer(self, peer_id: int, session=Depends(get_db)):
        """Remove a peer connection"""
        stmt = select(Peer).where(Peer.id == peer_id)
        peer = session.execute(stmt).scalars().first()
        if not peer:
            raise HTTPException(status_code=404, detail="Peer not found")
        
        session.delete(peer)
        session.commit()
        return PeerResponse.model_validate(peer)
