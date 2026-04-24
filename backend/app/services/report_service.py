from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.models.report import Report
from app.schemas.report import ReportCreate


class ReportService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def report_post(self, reporter_id: int, post_id: int, data: ReportCreate):
        post = self.repo.get_post(post_id, self.session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.user_id == reporter_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot report your own post")

        report = Report(reporter_id=reporter_id, post_id=post_id, reason=data.reason)
        self.repo.save_report(report, self.session)
        self.session.refresh(report)
        return report

    def list_unresolved(self):
        return self.repo.get_unresolved_reports(self.session)
