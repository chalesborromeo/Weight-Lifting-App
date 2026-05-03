from fastapi import APIRouter, Depends

from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.db.postgresql.factory import PostgreSQLFactory
from app.schemas.user import UserResponse
from app.api.deps import get_db
from app.core.security import get_current_user_id


def get_user_service(session=Depends(get_db)) -> UserService:
    repo = PostgreSQLFactory.create_db_repository()
    return UserService(repo, session)


class UserRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["users"])
        self.router.add_api_route("/", self.get_all, methods=["GET"], response_model=list[UserResponse])
        self.router.add_api_route("/register", self.create, methods=["POST"], response_model=UserResponse)
        self.router.add_api_route("/search", self.search, methods=["GET"], response_model=list[UserResponse])
        self.router.add_api_route("/me/streak", self.get_streak, methods=["GET"])
        self.router.add_api_route("/me/export", self.export, methods=["GET"])
        self.router.add_api_route("/suggestions", self.get_suggestions, methods=["GET"], response_model=list[UserResponse])
        self.router.add_api_route("/{user_id}", self.get_one, methods=["GET"], response_model=UserResponse)

    async def get_all(self, service: UserService = Depends(get_user_service)):
        return service.get_all_users()

    async def create(self, user: UserCreate, service: UserService = Depends(get_user_service)):
        return service.create_user(user)

    async def search(self, q: str, service: UserService = Depends(get_user_service)):
        return service.search_users(q)

    async def get_streak(
        self,
        user_id: int = Depends(get_current_user_id),
        service: UserService = Depends(get_user_service),
    ):
        return {"streak": service.get_streak(user_id)}

    async def get_suggestions(
        self,
        user_id: int = Depends(get_current_user_id),
        service: UserService = Depends(get_user_service),
    ):
        return service.get_suggestions(user_id)

    async def export(
        self,
        user_id: int = Depends(get_current_user_id),
        service: UserService = Depends(get_user_service),
    ):
        return service.export_data(user_id)

    async def get_one(self, user_id: int, service: UserService = Depends(get_user_service)):
        return service.get_user(user_id)
