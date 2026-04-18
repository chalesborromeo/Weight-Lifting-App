from typing import List

from pydantic import BaseModel

from app.schemas.user import UserResponse

class ClubCreate(BaseModel):
    owner_id: int
    name: str
    privacy: str

class ClubResponse(BaseModel):
    id: int
    name: str
    owner: UserResponse
    privacy: str
    members: List[UserResponse]

    model_config = {"from_attributes": True}
