from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.factory import PostgreSQLFactory
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationResponse
from app.core.security import get_current_user_id
from app.api.deps import get_db


def get_notification_service(session=Depends(get_db)) -> NotificationService:
    repo = PostgreSQLFactory.create_db_repository()
    return NotificationService(repo, session)


class NotificationRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/notifications", tags=["notifications"])
        self.router.add_api_route("/", self.list_mine, methods=["GET"], response_model=List[NotificationResponse])
        self.router.add_api_route("/{notification_id}/read", self.mark_read, methods=["PUT"], response_model=NotificationResponse)

    async def list_mine(
        self,
        user_id: int = Depends(get_current_user_id),
        service: NotificationService = Depends(get_notification_service),
    ):
        return service.list_mine(user_id)

    async def mark_read(
        self,
        notification_id: int,
        user_id: int = Depends(get_current_user_id),
        service: NotificationService = Depends(get_notification_service),
    ):
        return service.mark_read(user_id, notification_id)
