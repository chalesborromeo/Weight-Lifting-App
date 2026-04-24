from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.db.postgresql.factory import PostgreSQLFactory
from app.db.postgresql.connection import PostgreSQLConnection
from sqlalchemy import select
from app.models.notification import Notification
from pydantic import BaseModel
from datetime import datetime


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


class NotificationResponse(BaseModel):
    id: int
    message: str
    type: str
    time: datetime
    read: bool
    user_id: int

    model_config = {"from_attributes": True}


class NotificationMarkAsRead(BaseModel):
    read: bool


class NotificationsRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/notifications", tags=["notifications"])
        self.router.add_api_route("/user/{user_id}", self.get_notifications, methods=["GET"], response_model=List[NotificationResponse])
        self.router.add_api_route("/{notification_id}", self.get_notification, methods=["GET"], response_model=NotificationResponse)
        self.router.add_api_route("/{notification_id}", self.mark_as_read, methods=["PUT"], response_model=NotificationResponse)
        self.router.add_api_route("/{notification_id}", self.delete_notification, methods=["DELETE"], response_model=NotificationResponse)

    async def get_notifications(self, user_id: int, session=Depends(get_db)):
        """Get all notifications for a user"""
        stmt = select(Notification).where(Notification.user_id == user_id)
        notifications = session.execute(stmt).scalars().all()
        return [NotificationResponse.model_validate(n) for n in notifications]

    async def get_notification(self, notification_id: int, session=Depends(get_db)):
        """Get a specific notification"""
        stmt = select(Notification).where(Notification.id == notification_id)
        notification = session.execute(stmt).scalars().first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        return NotificationResponse.model_validate(notification)

    async def mark_as_read(self, notification_id: int, data: NotificationMarkAsRead, session=Depends(get_db)):
        """Mark a notification as read/unread"""
        stmt = select(Notification).where(Notification.id == notification_id)
        notification = session.execute(stmt).scalars().first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        notification.read = data.read
        session.commit()
        session.refresh(notification)
        return NotificationResponse.model_validate(notification)

    async def delete_notification(self, notification_id: int, session=Depends(get_db)):
        """Delete a notification"""
        stmt = select(Notification).where(Notification.id == notification_id)
        notification = session.execute(stmt).scalars().first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        session.delete(notification)
        session.commit()
        return NotificationResponse.model_validate(notification)
