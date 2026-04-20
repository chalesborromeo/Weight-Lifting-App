from pydantic import BaseModel

class SetCreate(BaseModel):
    weight: float
    reps: int

class SetResponse(BaseModel):
    id: int
    weight: float
    reps: int

    model_config = {"from_attributes": True}