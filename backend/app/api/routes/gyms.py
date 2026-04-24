from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory
from app.services.gym_service import GymService
from app.schemas.gym import GymCreate, GymResponse, NearbyGymResponse
from app.core.security import get_current_user_id


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


def get_gym_service(session=Depends(get_db)) -> GymService:
    repo = PostgreSQLFactory.create_db_repository()
    return GymService(repo, session)


class GymRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/gyms", tags=["gyms"])
        self.router.add_api_route("/", self.list_all, methods=["GET"], response_model=List[GymResponse])
        self.router.add_api_route("/", self.create, methods=["POST"], response_model=GymResponse)
        self.router.add_api_route("/nearby", self.list_nearby, methods=["GET"], response_model=List[NearbyGymResponse])
        self.router.add_api_route("/{gym_id}", self.get_one, methods=["GET"], response_model=GymResponse)

    async def list_all(self, service: GymService = Depends(get_gym_service)):
        return service.list_all()

    async def create(
        self,
        data: GymCreate,
        _user_id: int = Depends(get_current_user_id),
        service: GymService = Depends(get_gym_service),
    ):
        return service.create(data)

    async def list_nearby(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        _user_id: int = Depends(get_current_user_id),
        service: GymService = Depends(get_gym_service),
    ):
        """Gyms within radius_km of the given coordinates, sorted by distance (SRS 3.1.19)."""
        return service.list_nearby(lat, lng, radius_km)

    async def get_one(self, gym_id: int, service: GymService = Depends(get_gym_service)):
        return service.get(gym_id)
