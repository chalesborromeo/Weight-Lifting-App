from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.factory import PostgreSQLFactory
from app.services.body_metric_service import BodyMetricService
from app.schemas.body_metric import BodyMetricCreate, BodyMetricResponse
from app.core.security import get_current_user_id
from app.api.deps import get_db


def get_body_metric_service(session=Depends(get_db)) -> BodyMetricService:
    repo = PostgreSQLFactory.create_db_repository()
    return BodyMetricService(repo, session)


class BodyMetricRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/body-metrics", tags=["body-metrics"])
        self.router.add_api_route("/", self.list_mine, methods=["GET"], response_model=List[BodyMetricResponse])
        self.router.add_api_route("/", self.create, methods=["POST"], response_model=BodyMetricResponse)

    async def list_mine(
        self,
        user_id: int = Depends(get_current_user_id),
        service: BodyMetricService = Depends(get_body_metric_service),
    ):
        return service.list_metrics(user_id)

    async def create(
        self,
        data: BodyMetricCreate,
        user_id: int = Depends(get_current_user_id),
        service: BodyMetricService = Depends(get_body_metric_service),
    ):
        return service.create_metric(user_id, data)
