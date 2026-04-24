from pydantic import BaseModel
from typing import Optional


class SpotRequestCreate(BaseModel):
    spotter_id: int
    # Optional in the schema; the server uses the JWT identity as the requester
    # to prevent clients from spoofing requests on behalf of other users.
    requester_id: Optional[int] = None


class SpotRequestResponse(BaseModel):
    id: int
    status: bool
    spotter_id: int
    requester_id: int

    model_config = {"from_attributes": True}


class SpotRequestUpdate(BaseModel):
    status: bool
