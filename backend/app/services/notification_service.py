from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.models.notification import Notification


class NotificationService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def list_mine(self, user_id: int):
        return self.repo.get_notifications_by_user(user_id, self.session)

    def mark_read(self, user_id: int, notification_id: int):
        notif = self.repo.get_notification(notification_id, self.session)
        if not notif:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        if notif.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot mark another user's notification")

        notif.read = True
        self.session.flush()
        self.session.refresh(notif)
        return notif

    def create(self, user_id: int, message: str, notif_type: str):
        """Internal helper — other services call this to fan out notifications."""
        notif = Notification(user_id=user_id, message=message, type=notif_type)
        self.repo.save_notification(notif, self.session)
        self.session.refresh(notif)
        return notif
