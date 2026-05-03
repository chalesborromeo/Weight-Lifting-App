"""
Unit tests for Export Data use case (SRS 3.1.28)
- 3.1.28 Export Data
"""

import pytest
from unittest.mock import Mock
from datetime import datetime, date
from fastapi import HTTPException

from app.services.user_service import UserService
from app.models.user import User
from app.models.workout import Workout
from app.models.pr import PR
from app.models.body_metric import BodyMetric
from app.models.favorite_exercise import FavoriteExercise
from app.models.gym_checkin import GymCheckIn
from app.models.exercise import Exercise
from app.models.sets import Sets as Set


def make_user(id=1):
    u = User()
    u.id = id
    u.email = "test@test.com"
    u.password = "hashed"
    return u


def make_workout(id=1, user_id=1):
    e = Exercise()
    e.name = "Bench Press"
    s = Set()
    s.weight = 135.0
    s.reps = 10
    e.sets = [s]

    w = Workout()
    w.id = id
    w.user_id = user_id
    w.name = "Push Day"
    w.type = "Strength"
    w.duration = 60.0
    w.is_public = True
    w.created_at = datetime(2025, 1, 1)
    w.exercises = [e]
    return w


def make_pr(id=1, user_id=1):
    pr = PR()
    pr.id = id
    pr.user_id = user_id
    pr.exercise_name = "Bench Press"
    pr.weight = 225.0
    pr.reps = 5
    pr.date = date(2025, 1, 1)
    return pr


def make_metric(id=1, user_id=1):
    m = BodyMetric()
    m.id = id
    m.user_id = user_id
    m.weight = 180.0
    m.recorded_at = datetime(2025, 1, 1)
    return m


def make_favorite(id=1, user_id=1, name="Bench Press"):
    f = FavoriteExercise()
    f.id = id
    f.user_id = user_id
    f.name = name
    return f


def make_checkin(id=1, user_id=1):
    c = GymCheckIn()
    c.id = id
    c.user_id = user_id
    c.gym_name = "Planet Fitness"
    c.gym_address = "123 Main St"
    c.checked_in_at = datetime(2025, 1, 1)
    return c


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def mock_session():
    return Mock()


@pytest.fixture
def service(mock_repo, mock_session):
    return UserService(mock_repo, mock_session)


class TestExportData:
    def test_export_includes_all_sections(self, service, mock_repo):
        user = make_user()
        mock_repo.get_user.return_value = user
        mock_repo.get_profile_by_user.return_value = None
        mock_repo.get_users_workouts.return_value = [make_workout()]
        mock_repo.get_prs_by_user.return_value = [make_pr()]
        mock_repo.get_body_metrics_by_user.return_value = [make_metric()]
        mock_repo.get_favorite_exercises_by_user.return_value = [make_favorite()]
        mock_repo.get_checkins_by_user.return_value = [make_checkin()]

        result = service.export_data(user_id=1)

        assert "user" in result
        assert "workouts" in result
        assert "personal_records" in result
        assert "body_metrics" in result
        assert "favorite_exercises" in result
        assert "gym_checkins" in result

    def test_export_workout_includes_exercises_and_sets(self, service, mock_repo):
        user = make_user()
        mock_repo.get_user.return_value = user
        mock_repo.get_profile_by_user.return_value = None
        mock_repo.get_users_workouts.return_value = [make_workout()]
        mock_repo.get_prs_by_user.return_value = []
        mock_repo.get_body_metrics_by_user.return_value = []
        mock_repo.get_favorite_exercises_by_user.return_value = []
        mock_repo.get_checkins_by_user.return_value = []

        result = service.export_data(user_id=1)

        workouts = result["workouts"]
        assert len(workouts) == 1
        assert workouts[0]["name"] == "Push Day"
        assert len(workouts[0]["exercises"]) == 1
        assert workouts[0]["exercises"][0]["name"] == "Bench Press"
        assert workouts[0]["exercises"][0]["sets"][0]["weight"] == 135.0

    def test_export_includes_pr_data(self, service, mock_repo):
        mock_repo.get_user.return_value = make_user()
        mock_repo.get_profile_by_user.return_value = None
        mock_repo.get_users_workouts.return_value = []
        mock_repo.get_prs_by_user.return_value = [make_pr()]
        mock_repo.get_body_metrics_by_user.return_value = []
        mock_repo.get_favorite_exercises_by_user.return_value = []
        mock_repo.get_checkins_by_user.return_value = []

        result = service.export_data(user_id=1)

        prs = result["personal_records"]
        assert len(prs) == 1
        assert prs[0]["exercise"] == "Bench Press"
        assert prs[0]["weight"] == 225.0

    def test_export_includes_checkins(self, service, mock_repo):
        mock_repo.get_user.return_value = make_user()
        mock_repo.get_profile_by_user.return_value = None
        mock_repo.get_users_workouts.return_value = []
        mock_repo.get_prs_by_user.return_value = []
        mock_repo.get_body_metrics_by_user.return_value = []
        mock_repo.get_favorite_exercises_by_user.return_value = []
        mock_repo.get_checkins_by_user.return_value = [make_checkin()]

        result = service.export_data(user_id=1)

        checkins = result["gym_checkins"]
        assert len(checkins) == 1
        assert checkins[0]["gym_name"] == "Planet Fitness"

    def test_export_raises_404_for_unknown_user(self, service, mock_repo):
        mock_repo.get_user.return_value = None

        with pytest.raises(HTTPException) as exc:
            service.export_data(user_id=999)

        assert exc.value.status_code == 404
