from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.factory import PostgreSQLFactory
from app.services.report_service import ReportService
from app.schemas.report import ReportCreate, ReportResponse
from app.core.security import get_current_user_id
from app.api.deps import get_db


def get_report_service(session=Depends(get_db)) -> ReportService:
    repo = PostgreSQLFactory.create_db_repository()
    return ReportService(repo, session)


class ReportRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/reports", tags=["reports"])
        self.router.add_api_route("/posts/{post_id}", self.report_post, methods=["POST"], response_model=ReportResponse)
        self.router.add_api_route("/unresolved", self.list_unresolved, methods=["GET"], response_model=List[ReportResponse])

    async def report_post(
        self,
        post_id: int,
        data: ReportCreate,
        user_id: int = Depends(get_current_user_id),
        service: ReportService = Depends(get_report_service),
    ):
        """Report a post for inappropriate content (SRS 3.1.30)."""
        return service.report_post(user_id, post_id, data)

    async def list_unresolved(
        self,
        _user_id: int = Depends(get_current_user_id),
        service: ReportService = Depends(get_report_service),
    ):
        """Admin/moderator view of unresolved reports."""
        return service.list_unresolved()
