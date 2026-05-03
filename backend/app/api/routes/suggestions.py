from fastapi import APIRouter, Depends

from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory
from app.services.suggestion_service import SuggestionService
from app.schemas.suggestion import WorkoutSuggestion
from app.core.security import get_current_user_id


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


def get_suggestion_service(session=Depends(get_db)) -> SuggestionService:
    repo = PostgreSQLFactory.create_db_repository()
    return SuggestionService(repo, session)


class SuggestionRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/suggestions", tags=["suggestions"])

        self.router.add_api_route(
            "/workout",
            self.get_workout_suggestion,
            methods=["GET"],
            response_model=WorkoutSuggestion
        )

    async def get_workout_suggestion(
        self,
        user_id: int = Depends(get_current_user_id),
        service: SuggestionService = Depends(get_suggestion_service),
    ):
        """
        Get personalized workout suggestion based on favorite exercises and recent performance.
        Uses progressive overload principles.
        """
        return service.get_workout_suggestion(user_id)
