from typing import Optional, Any
from pydantic import BaseModel, EmailStr, model_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = {"from_attributes": True}

    @model_validator(mode='before')
    @classmethod
    def pull_profile_fields(cls, data: Any):
        if hasattr(data, 'profile') and data.profile is not None:
            return {
                'id': data.id,
                'email': data.email,
                'first_name': data.profile.first_name,
                'last_name': data.profile.last_name,
            }
        return data
