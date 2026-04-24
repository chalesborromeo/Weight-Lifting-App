from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory
from app.services.favorite_exercise_service import FavoriteExerciseService
from app.schemas.favorite_exercise import FavoriteExerciseCreate, FavoriteExerciseResponse
from app.core.security import get_current_user_id


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


def get_favorite_exercise_service(session=Depends(get_db)) -> FavoriteExerciseService:
    repo = PostgreSQLFactory.create_db_repository()
    return FavoriteExerciseService(repo, session)


class FavoriteExerciseRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/favorite-exercises", tags=["favorite-exercises"])
        self.router.add_api_route("/", self.list_mine, methods=["GET"], response_model=List[FavoriteExerciseResponse])
        self.router.add_api_route("/", self.add, methods=["POST"], response_model=FavoriteExerciseResponse)
        self.router.add_api_route("/{favorite_id}", self.remove, methods=["DELETE"])

    async def list_mine(
        self,
        user_id: int = Depends(get_current_user_id),
        service: FavoriteExerciseService = Depends(get_favorite_exercise_service),
    ):
        return service.list_favorites(user_id)

    async def add(
        self,
        data: FavoriteExerciseCreate,
        user_id: int = Depends(get_current_user_id),
        service: FavoriteExerciseService = Depends(get_favorite_exercise_service),
    ):
        return service.add_favorite(user_id, data)

    async def remove(
        self,
        favorite_id: int,
        user_id: int = Depends(get_current_user_id),
        service: FavoriteExerciseService = Depends(get_favorite_exercise_service),
    ):
        return service.remove_favorite(user_id, favorite_id)
