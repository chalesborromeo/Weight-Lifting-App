from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.factory import PostgreSQLFactory
from app.services.peer_service import PeerService
from app.schemas.peer import PeerResponse
from app.core.security import get_current_user_id
from app.api.deps import get_db


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
