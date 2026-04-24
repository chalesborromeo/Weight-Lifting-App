from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from app.schemas.user import UserResponse
from app.schemas.workout import WorkoutResponse


class CommentCreate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: int
    text: str
    date: datetime
    user_id: int
    user: UserResponse

    model_config = {"from_attributes": True}


class PostCreate(BaseModel):
    text: Optional[str] = None
    workout_id: Optional[int] = None
    club_id: Optional[int] = None


class PostResponse(BaseModel):
    id: int
    date: datetime
    text: Optional[str] = None
    likes: int
    user_id: int
    user: UserResponse
    workout_id: Optional[int] = None
    workout: Optional[WorkoutResponse] = None
    club_id: Optional[int] = None
    comments: List[CommentResponse] = []

    model_config = {"from_attributes": True}
