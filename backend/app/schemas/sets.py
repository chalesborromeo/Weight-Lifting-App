from pydantic import BaseModel, Field

class SetCreate(BaseModel):
    weight: float = Field(gt=0, description="Weight must be positive")
    reps: int = Field(gt=0, description="Reps must be positive")

class SetResponse(BaseModel):
    id: int
    weight: float
    reps: int

    model_config = {"from_attributes": True}