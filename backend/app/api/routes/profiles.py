from fastapi import APIRouter, Depends

from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory
from app.services.profile_service import ProfileService
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.core.security import get_current_user_id


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


def get_profile_service(session=Depends(get_db)) -> ProfileService:
    repo = PostgreSQLFactory.create_db_repository()
    return ProfileService(repo, session)


class ProfileRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/profiles", tags=["profiles"])
        self.router.add_api_route("/me", self.get_me, methods=["GET"], response_model=ProfileResponse)
        self.router.add_api_route("/me", self.create_me, methods=["POST"], response_model=ProfileResponse)
        self.router.add_api_route("/me", self.update_me, methods=["PUT"], response_model=ProfileResponse)
        self.router.add_api_route("/me/gym/{gym_id}", self.set_gym, methods=["PUT"], response_model=ProfileResponse)

    async def get_me(
        self,
        user_id: int = Depends(get_current_user_id),
        service: ProfileService = Depends(get_profile_service),
    ):
        return service.get_my_profile(user_id)

    async def create_me(
        self,
        data: ProfileCreate,
        user_id: int = Depends(get_current_user_id),
        service: ProfileService = Depends(get_profile_service),
    ):
        return service.create_profile(user_id, data)

    async def update_me(
        self,
        data: ProfileUpdate,
        user_id: int = Depends(get_current_user_id),
        service: ProfileService = Depends(get_profile_service),
    ):
        return service.update_profile(user_id, data)

    async def set_gym(
        self,
        gym_id: int,
        user_id: int = Depends(get_current_user_id),
        service: ProfileService = Depends(get_profile_service),
    ):
        return service.set_gym(user_id, gym_id)
