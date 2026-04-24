from pydantic import BaseModel


class FavoriteExerciseCreate(BaseModel):
    name: str


class FavoriteExerciseResponse(BaseModel):
    id: int
    name: str
    user_id: int

    model_config = {"from_attributes": True}
