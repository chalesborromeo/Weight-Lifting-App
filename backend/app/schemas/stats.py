from pydantic import BaseModel
from datetime import datetime
from typing import List

from app.schemas.pr import PRResponse


class VolumeStatsResponse(BaseModel):
    total_workouts: int
    total_sets: int
    total_reps: int
    total_volume: float
    start_date: datetime
    end_date: datetime


class PeriodicVolumeResponse(BaseModel):
    period_start: datetime
    total_sets: int
    total_reps: int
    total_volume: float


class PRProgressionResponse(BaseModel):
    exercise_name: str
    prs: List[PRResponse]
    pr_count: int
    start_date: datetime
    end_date: datetime


class WorkoutStatsResponse(BaseModel):
    volume: VolumeStatsResponse
    pr_count: int
    prs: List[PRResponse]
