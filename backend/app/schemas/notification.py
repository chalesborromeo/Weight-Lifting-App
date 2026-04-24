from datetime import datetime
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: int
    message: str
    type: str
    time: datetime
    read: bool
    user_id: int

    model_config = {"from_attributes": True}
