from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory
from app.services.spotter_service import SpotterService
from app.schemas.spot_request import SpotRequestCreate, SpotRequestResponse
from app.core.security import get_current_user_id


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


def get_spotter_service(session=Depends(get_db)) -> SpotterService:
    repo = PostgreSQLFactory.create_db_repository()
    return SpotterService(repo, session)


class SpotterRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/spotters", tags=["spotters"])
        self.router.add_api_route("/", self.send_request, methods=["POST"], response_model=SpotRequestResponse)
        self.router.add_api_route("/incoming", self.list_incoming, methods=["GET"], response_model=List[SpotRequestResponse])
        self.router.add_api_route("/outgoing", self.list_outgoing, methods=["GET"], response_model=List[SpotRequestResponse])
        self.router.add_api_route("/{request_id}/accept", self.accept, methods=["PUT"], response_model=SpotRequestResponse)
        self.router.add_api_route("/{request_id}/decline", self.decline, methods=["DELETE"])

    async def send_request(
        self,
        data: SpotRequestCreate,
        user_id: int = Depends(get_current_user_id),
        service: SpotterService = Depends(get_spotter_service),
    ):
        """Request another user as a spotter (SRS 3.1.22)."""
        return service.send_request(user_id, data)

    async def list_incoming(
        self,
        user_id: int = Depends(get_current_user_id),
        service: SpotterService = Depends(get_spotter_service),
    ):
        return service.list_incoming(user_id)

    async def list_outgoing(
        self,
        user_id: int = Depends(get_current_user_id),
        service: SpotterService = Depends(get_spotter_service),
    ):
        return service.list_outgoing(user_id)

    async def accept(
        self,
        request_id: int,
        user_id: int = Depends(get_current_user_id),
        service: SpotterService = Depends(get_spotter_service),
    ):
        return service.accept_request(user_id, request_id)

    async def decline(
        self,
        request_id: int,
        user_id: int = Depends(get_current_user_id),
        service: SpotterService = Depends(get_spotter_service),
    ):
        return service.decline_request(user_id, request_id)
