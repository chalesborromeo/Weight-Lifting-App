from datetime import datetime
from pydantic import BaseModel


class ReportCreate(BaseModel):
    reason: str


class ReportResponse(BaseModel):
    id: int
    reason: str
    created_at: datetime
    resolved: bool
    reporter_id: int
    post_id: int

    model_config = {"from_attributes": True}
