from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.models.peer import Peer


class PeerService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def send_request(self, user_id: int, peer_id: int):
        if user_id == peer_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot add yourself")

        existing = self.repo.get_peer(user_id, peer_id, self.session)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Peer request already exists")

        peer = Peer()
        peer.user_id = user_id
        peer.peer_id = peer_id
        peer.status = "pending"
        self.repo.save_peer(peer, self.session)
        self.session.refresh(peer)
        return peer

    def accept_request(self, user_id: int, peer_id: int):
        # Find the incoming request (where peer_id sent request to user_id)
        request = self.repo.get_peer(peer_id, user_id, self.session)
        if not request or request.status != "pending":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No pending request found")

        request.status = "accepted"

        # Create reciprocal peer relationship
        reciprocal = self.repo.get_peer(user_id, peer_id, self.session)
        if not reciprocal:
            reciprocal = Peer()
            reciprocal.user_id = user_id
            reciprocal.peer_id = peer_id
            reciprocal.status = "accepted"
            self.repo.save_peer(reciprocal, self.session)

        self.session.flush()
        self.session.refresh(request)
        return request

    def reject_request(self, user_id: int, peer_id: int):
        request = self.repo.get_peer(peer_id, user_id, self.session)
        if not request or request.status != "pending":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No pending request found")
        self.repo.delete_peer(request.id, self.session)
        return {"message": "Request rejected"}

    def get_peers(self, user_id: int):
        return self.repo.get_peers_by_user(user_id, "accepted", self.session)

    def get_pending(self, user_id: int):
        return self.repo.get_pending_for_user(user_id, self.session)

    def remove_peer(self, user_id: int, peer_id: int):
        # Remove both directions
        p1 = self.repo.get_peer(user_id, peer_id, self.session)
        p2 = self.repo.get_peer(peer_id, user_id, self.session)
        if p1:
            self.repo.delete_peer(p1.id, self.session)
        if p2:
            self.repo.delete_peer(p2.id, self.session)
        return {"message": "Peer removed"}
