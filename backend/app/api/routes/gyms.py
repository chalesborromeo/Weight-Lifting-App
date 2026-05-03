from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.factory import PostgreSQLFactory
from app.services.gym_service import GymService
from app.schemas.gym import GymCreate, GymResponse, NearbyGymResponse, GymCheckInCreate, GymCheckInResponse
from app.core.security import get_current_user_id
from app.api.deps import get_db


def get_gym_service(session=Depends(get_db)) -> GymService:
    repo = PostgreSQLFactory.create_db_repository()
    return GymService(repo, session)


class GymRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/gyms", tags=["gyms"])
        self.router.add_api_route("/", self.list_all, methods=["GET"], response_model=List[GymResponse])
        self.router.add_api_route("/", self.create, methods=["POST"], response_model=GymResponse)
        self.router.add_api_route("/nearby", self.list_nearby, methods=["GET"], response_model=List[NearbyGymResponse])
        self.router.add_api_route("/checkins", self.list_checkins, methods=["GET"], response_model=List[GymCheckInResponse])
        self.router.add_api_route("/checkins", self.checkin, methods=["POST"], response_model=GymCheckInResponse)
        self.router.add_api_route("/checkins/{checkin_id}", self.delete_checkin, methods=["DELETE"], response_model=GymCheckInResponse)
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
        service: GymService = Depends(get_gym_service),
    ):
        return service.list_nearby(lat, lng, radius_km)

    async def list_checkins(
        self,
        user_id: int = Depends(get_current_user_id),
        service: GymService = Depends(get_gym_service),
    ):
        return service.list_checkins(user_id)

    async def checkin(
        self,
        data: GymCheckInCreate,
        user_id: int = Depends(get_current_user_id),
        service: GymService = Depends(get_gym_service),
    ):
        return service.checkin(user_id, data)

    async def delete_checkin(
        self,
        checkin_id: int,
        user_id: int = Depends(get_current_user_id),
        service: GymService = Depends(get_gym_service),
    ):
        return service.delete_checkin(checkin_id, user_id)

    async def get_one(self, gym_id: int, service: GymService = Depends(get_gym_service)):
        return service.get(gym_id)
