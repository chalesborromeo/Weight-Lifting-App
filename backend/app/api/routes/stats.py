from typing import List, Literal
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory
from app.services.stats_service import StatsService
from app.schemas.stats import (
    VolumeStatsResponse,
    PeriodicVolumeResponse,
    PRProgressionResponse,
    WorkoutStatsResponse
)
from app.schemas.pr import PRResponse
from app.core.security import get_current_user_id


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


def get_stats_service(session=Depends(get_db)) -> StatsService:
    repo = PostgreSQLFactory.create_db_repository()
    return StatsService(repo, session)


class StatsRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/stats", tags=["stats"])

        # Volume endpoints
        self.router.add_api_route(
            "/volume",
            self.get_volume,
            methods=["GET"],
            response_model=VolumeStatsResponse
        )
        self.router.add_api_route(
            "/volume/periodic",
            self.get_periodic_volume,
            methods=["GET"],
            response_model=List[PeriodicVolumeResponse]
        )

        # PR endpoints
        self.router.add_api_route(
            "/prs",
            self.get_prs,
            methods=["GET"],
            response_model=List[PRResponse]
        )
        self.router.add_api_route(
            "/prs/progression",
            self.get_pr_progression,
            methods=["GET"],
            response_model=PRProgressionResponse
        )

        # Combined overview
        self.router.add_api_route(
            "/overview",
            self.get_overview,
            methods=["GET"],
            response_model=WorkoutStatsResponse
        )

    async def get_volume(
        self,
        start_date: datetime = Query(..., description="Start of date range"),
        end_date: datetime = Query(..., description="End of date range"),
        user_id: int = Depends(get_current_user_id),
        service: StatsService = Depends(get_stats_service),
    ):
        """Get aggregate volume statistics for date range."""
        return service.get_volume_stats(user_id, start_date, end_date)

    async def get_periodic_volume(
        self,
        start_date: datetime = Query(..., description="Start of date range"),
        end_date: datetime = Query(..., description="End of date range"),
        period: Literal["week", "month"] = Query("week", description="Grouping period"),
        user_id: int = Depends(get_current_user_id),
        service: StatsService = Depends(get_stats_service),
    ):
        """Get volume statistics grouped by week or month."""
        return service.get_volume_by_period(user_id, start_date, end_date, period)

    async def get_prs(
        self,
        start_date: datetime = Query(..., description="Start of date range"),
        end_date: datetime = Query(..., description="End of date range"),
        user_id: int = Depends(get_current_user_id),
        service: StatsService = Depends(get_stats_service),
    ):
        """Get all PRs achieved within date range."""
        return service.get_pr_stats(user_id, start_date, end_date)

    async def get_pr_progression(
        self,
        exercise_name: str = Query(..., description="Exercise name to track"),
        start_date: datetime = Query(..., description="Start of date range"),
        end_date: datetime = Query(..., description="End of date range"),
        user_id: int = Depends(get_current_user_id),
        service: StatsService = Depends(get_stats_service),
    ):
        """Get PR progression for a specific exercise over time."""
        return service.get_pr_progression(user_id, exercise_name, start_date, end_date)

    async def get_overview(
        self,
        start_date: datetime = Query(..., description="Start of date range"),
        end_date: datetime = Query(..., description="End of date range"),
        user_id: int = Depends(get_current_user_id),
        service: StatsService = Depends(get_stats_service),
    ):
        """Get combined overview with volume and PR stats."""
        return service.get_combined_stats(user_id, start_date, end_date)
