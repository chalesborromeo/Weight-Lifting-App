from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.db.postgresql.factory import PostgreSQLFactory
from app.db.postgresql.connection import PostgreSQLConnection
from sqlalchemy import select
from app.models.peer import Peer
from pydantic import BaseModel
from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory
from app.services.peer_service import PeerService
from app.schemas.peer import PeerResponse
from app.core.security import get_current_user_id


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
def get_peer_service(session=Depends(get_db)) -> PeerService:
    repo = PostgreSQLFactory.create_db_repository()
    return PeerService(repo, session)


class PeerRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/peers", tags=["peers"])
        self.router.add_api_route("/", self.get_peers, methods=["GET"], response_model=List[PeerResponse])
        self.router.add_api_route("/pending", self.get_pending, methods=["GET"], response_model=List[PeerResponse])
        self.router.add_api_route("/{peer_id}", self.send_request, methods=["POST"], response_model=PeerResponse)
        self.router.add_api_route("/{peer_id}/accept", self.accept, methods=["PUT"])
        self.router.add_api_route("/{peer_id}", self.remove, methods=["DELETE"])

    async def get_peers(
        self,
        user_id: int = Depends(get_current_user_id),
        service: PeerService = Depends(get_peer_service),
    ):
        return service.get_peers(user_id)

    async def get_pending(
        self,
        user_id: int = Depends(get_current_user_id),
        service: PeerService = Depends(get_peer_service),
    ):
        return service.get_pending(user_id)

    async def send_request(
        self,
        peer_id: int,
        user_id: int = Depends(get_current_user_id),
        service: PeerService = Depends(get_peer_service),
    ):
        return service.send_request(user_id, peer_id)

    async def accept(
        self,
        peer_id: int,
        user_id: int = Depends(get_current_user_id),
        service: PeerService = Depends(get_peer_service),
    ):
        return service.accept_request(user_id, peer_id)

    async def remove(
        self,
        peer_id: int,
        user_id: int = Depends(get_current_user_id),
        service: PeerService = Depends(get_peer_service),
    ):
        return service.remove_peer(user_id, peer_id)
