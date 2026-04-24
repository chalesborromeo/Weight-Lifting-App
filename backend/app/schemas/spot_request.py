from pydantic import BaseModel
from typing import Optional


class SpotRequestCreate(BaseModel):
    spotter_id: int
    requester_id: int


class SpotRequestResponse(BaseModel):
    id: int
    status: bool
    spotter_id: int
    requester_id: int

    model_config = {"from_attributes": True}


class SpotRequestUpdate(BaseModel):
    status: bool
