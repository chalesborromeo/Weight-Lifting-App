from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CommentCreate(BaseModel):
    user_id: int
    post_id: int
    text: str


class CommentResponse(BaseModel):
    id: int
    text: str
    date: datetime
    user_id: int

    model_config = {"from_attributes": True}


class PostCreate(BaseModel):
    user_id: int
    text: Optional[str] = None
    workout_id: Optional[int] = None
    club_id: Optional[int] = None


class PostResponse(BaseModel):
    id: int
    date: datetime
    text: Optional[str] = None
    likes: int
    user_id: int
    workout_id: Optional[int] = None
    club_id: Optional[int] = None
    comments: List[CommentResponse] = []

    model_config = {"from_attributes": True}


class PostUpdate(BaseModel):
    text: Optional[str] = None
    likes: Optional[int] = None
