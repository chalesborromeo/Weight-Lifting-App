from typing import List, Optional

from pydantic import BaseModel

from app.schemas.user import UserResponse

class ClubCreate(BaseModel):
    owner_id: int
    name: str
    description: Optional[str] = None
    privacy: str

class ClubResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner: UserResponse
    privacy: str
    members: List[UserResponse]

    model_config = {"from_attributes": True}
