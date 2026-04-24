from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import UserResponse


class PeerResponse(BaseModel):
    id: int
    status: str
    created_at: datetime
    user_id: int
    peer_id: int
    user: UserResponse
    peer: UserResponse

    model_config = {"from_attributes": True}
