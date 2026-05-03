from pydantic import BaseModel
from typing import List, Optional


class ExerciseSuggestion(BaseModel):
    exercise_name: str
    suggested_sets: int
    suggested_reps: int
    suggested_weight: Optional[float]
    previous_best_weight: Optional[float]
    previous_best_reps: Optional[int]
    rationale: str


class WorkoutSuggestion(BaseModel):
    workout_name: str
    workout_type: str
    estimated_duration: float
    exercises: List[ExerciseSuggestion]
    total_exercises: int
