from datetime import datetime
from typing import List, Literal
from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.schemas.stats import (
    VolumeStatsResponse,
    PeriodicVolumeResponse,
    PRProgressionResponse,
    WorkoutStatsResponse
)


class StatsService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def get_volume_stats(self, user_id: int, start_date: datetime, end_date: datetime) -> VolumeStatsResponse:
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date must be before end_date"
            )

        result = self.repo.get_workout_volume_stats(user_id, start_date, end_date, self.session)

        return VolumeStatsResponse(
            total_workouts=result.total_workouts or 0,
            total_sets=result.total_sets or 0,
            total_reps=result.total_reps or 0,
            total_volume=result.total_volume or 0.0,
            start_date=start_date,
            end_date=end_date
        )

    def get_volume_by_period(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime,
        period: Literal["week", "month"]
    ) -> List[PeriodicVolumeResponse]:
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date must be before end_date"
            )

        results = self.repo.get_workout_volume_by_period(
            user_id, start_date, end_date, period, self.session
        )

        return [
            PeriodicVolumeResponse(
                period_start=r.period_start,
                total_sets=r.total_sets or 0,
                total_reps=r.total_reps or 0,
                total_volume=r.total_volume or 0.0
            )
            for r in results
        ]

    def get_pr_stats(self, user_id: int, start_date: datetime, end_date: datetime):
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date must be before end_date"
            )

        prs = self.repo.get_prs_in_date_range(user_id, start_date, end_date, self.session)
        return prs

    def get_pr_progression(
        self,
        user_id: int,
        exercise_name: str,
        start_date: datetime,
        end_date: datetime
    ) -> PRProgressionResponse:
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date must be before end_date"
            )

        prs = self.repo.get_pr_progression_by_exercise(
            user_id, exercise_name, start_date, end_date, self.session
        )

        return PRProgressionResponse(
            exercise_name=exercise_name,
            prs=prs,
            pr_count=len(prs),
            start_date=start_date,
            end_date=end_date
        )

    def get_combined_stats(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> WorkoutStatsResponse:
        volume = self.get_volume_stats(user_id, start_date, end_date)
        prs = self.get_pr_stats(user_id, start_date, end_date)

        return WorkoutStatsResponse(
            volume=volume,
            pr_count=len(prs),
            prs=prs
        )
