from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.models.spot_Request import Spot_Request
from app.schemas.spot_request import SpotRequestCreate
from app.services.notification_service import NotificationService


class SpotterService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session
        self.notifications = NotificationService(repo, session)

    def send_request(self, requester_id: int, data: SpotRequestCreate):
        if requester_id == data.spotter_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot request yourself as spotter")

        spotter = self.repo.get_user(data.spotter_id, self.session)
        if not spotter:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spotter not found")

        req = Spot_Request(requester_id=requester_id, spotter_id=data.spotter_id, status=False)
        self.repo.save_spot_request(req, self.session)
        self.session.refresh(req)

        self.notifications.create(
            user_id=data.spotter_id,
            message=f"User {requester_id} requested you as a spotter",
            notif_type="spot_request",
        )
        return req

    def accept_request(self, spotter_id: int, request_id: int):
        req = self.repo.get_spot_request(request_id, self.session)
        if not req:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spot request not found")
        if req.spotter_id != spotter_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the target spotter")

        req.status = True
        self.session.flush()
        self.session.refresh(req)

        self.notifications.create(
            user_id=req.requester_id,
            message=f"User {spotter_id} accepted your spot request",
            notif_type="spot_accepted",
        )
        return req

    def decline_request(self, spotter_id: int, request_id: int):
        req = self.repo.get_spot_request(request_id, self.session)
        if not req:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spot request not found")
        if req.spotter_id != spotter_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the target spotter")

        requester_id = req.requester_id
        self.repo.delete_spot_request(request_id, self.session)

        self.notifications.create(
            user_id=requester_id,
            message=f"User {spotter_id} declined your spot request",
            notif_type="spot_declined",
        )
        return {"message": "Spot request declined"}

    def list_incoming(self, user_id: int):
        return self.repo.get_incoming_spot_requests(user_id, self.session)

    def list_outgoing(self, user_id: int):
        return self.repo.get_outgoing_spot_requests(user_id, self.session)
