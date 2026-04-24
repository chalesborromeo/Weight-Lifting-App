from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory
from app.services.pr_service import PRService
from app.schemas.pr import PRCreate, PRResponse
from app.core.security import get_current_user_id


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


def get_pr_service(session=Depends(get_db)) -> PRService:
    repo = PostgreSQLFactory.create_db_repository()
    return PRService(repo, session)


class PRRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/prs", tags=["prs"])
        self.router.add_api_route("/", self.list_mine, methods=["GET"], response_model=List[PRResponse])
        self.router.add_api_route("/", self.create, methods=["POST"], response_model=PRResponse)
        self.router.add_api_route("/leaderboard", self.leaderboard, methods=["GET"], response_model=List[PRResponse])
        self.router.add_api_route("/{pr_id}", self.delete, methods=["DELETE"])

    async def list_mine(
        self,
        user_id: int = Depends(get_current_user_id),
        service: PRService = Depends(get_pr_service),
    ):
        return service.list_prs(user_id)

    async def create(
        self,
        data: PRCreate,
        user_id: int = Depends(get_current_user_id),
        service: PRService = Depends(get_pr_service),
    ):
        return service.create_pr(user_id, data)

    async def leaderboard(
        self,
        exercise: str,
        limit: int = 10,
        service: PRService = Depends(get_pr_service),
    ):
        """Top PRs for a specific exercise (SRS 3.1.18)."""
        return service.leaderboard(exercise, limit)

    async def delete(
        self,
        pr_id: int,
        user_id: int = Depends(get_current_user_id),
        service: PRService = Depends(get_pr_service),
    ):
        return service.delete_pr(user_id, pr_id)
