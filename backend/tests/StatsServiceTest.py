import unittest
from unittest.mock import MagicMock
from datetime import datetime
from fastapi import HTTPException

from app.services.stats_service import StatsService


class TestViewWeeklyMonthlyStats(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_session = MagicMock()
        self.service = StatsService(self.mock_repo, self.mock_session)

    # Basis Path Testing - Path 1
    # start_date is after end_date, invalid range should raise 400 error
    def test_invalid_date_range_raises_exception(self):
        start = datetime(2025, 5, 1)
        end = datetime(2025, 4, 1)
        with self.assertRaises(HTTPException) as ctx:
            self.service.get_volume_by_period(1, start, end, "week")
        self.assertEqual(ctx.exception.status_code, 400)

    # Basis Path Testing - Path 2:
    # Valid date range but no workouts logged, should return empty list
    def test_valid_dates_no_workouts_returns_empty_list(self):
        start = datetime(2025, 4, 1)
        end = datetime(2025, 5, 1)
        self.mock_repo.get_workout_volume_by_period.return_value = []
        result = self.service.get_volume_by_period(1, start, end, "week")
        self.assertEqual(result, [])

    # Basis Path Testing - Path 3
    # Valid date range with workouts logged, should return weekly volume stats
    def test_valid_dates_with_workouts_returns_weekly_stats(self):
        start = datetime(2025, 4, 1)
        end = datetime(2025, 5, 1)
        mock_row = MagicMock()
        mock_row.period_start = datetime(2025, 4, 7)
        mock_row.total_sets = 15
        mock_row.total_reps = 100
        mock_row.total_volume = 5000.0
        self.mock_repo.get_workout_volume_by_period.return_value = [mock_row]
        result = self.service.get_volume_by_period(1, start, end, "week")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].total_volume, 5000.0)
        self.assertEqual(result[0].total_sets, 15)
        self.assertEqual(result[0].total_reps, 100)

    # Basis Path Testing - Path 3 (monthly variant)
    # Same path with monthly period grouping instead of weekly
    def test_valid_dates_with_workouts_returns_monthly_stats(self):
        start = datetime(2025, 1, 1)
        end = datetime(2025, 5, 1)
        mock_row = MagicMock()
        mock_row.period_start = datetime(2025, 3, 1)
        mock_row.total_sets = 60
        mock_row.total_reps = 400
        mock_row.total_volume = 20000.0
        self.mock_repo.get_workout_volume_by_period.return_value = [mock_row]
        result = self.service.get_volume_by_period(1, start, end, "month")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].total_volume, 20000.0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
