from pydantic import BaseModel

from app.schemas.user import UserResponse


class SpotRequestCreate(BaseModel):
    # Requester is always the JWT identity (server-side), so clients only
    # pick the target spotter.
    spotter_id: int


class SpotRequestResponse(BaseModel):
    id: int
    status: bool
    spotter_id: int
    requester_id: int
    spotter: UserResponse
    requester: UserResponse

    model_config = {"from_attributes": True}


class SpotRequestUpdate(BaseModel):
    status: bool
