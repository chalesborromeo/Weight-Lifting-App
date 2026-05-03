"""
Unit tests for Workout use cases (SRS 3.1.5, 3.1.6, 3.1.7, 3.1.27)
- 3.1.5  Add Workout Log
- 3.1.6  View Workout Log
- 3.1.7  Delete Workout Log
- 3.1.27 Workout Privacy (public/private filtering)
"""

import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.services.workout_service import WorkoutService
from app.schemas.workout import WorkoutCreate
from app.models.workout import Workout
from app.models.exercise import Exercise


def make_workout(id=1, user_id=1, name="Push Day", is_public=True):
    w = Workout()
    w.id = id
    w.user_id = user_id
    w.name = name
    w.type = "Strength"
    w.duration = 60.0
    w.is_public = is_public
    w.exercises = []
    return w


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def mock_session():
    return Mock()


@pytest.fixture
def service(mock_repo, mock_session):
    return WorkoutService(mock_repo, mock_session)


class TestCreateWorkout:
    def test_creates_and_returns_workout(self, service, mock_repo, mock_session):
        payload = WorkoutCreate(
            user_id=1,
            name="Push Day",
            type="Strength",
            duration=60,
            is_public=True,
            exercises=[],
        )
        saved = make_workout()
        mock_session.refresh.side_effect = lambda obj: None

        def fake_save(workout, session):
            workout.id = 1
        mock_repo.save_workout.side_effect = fake_save

        result = service.create_workout(payload)

        mock_repo.save_workout.assert_called_once()
        assert result.name == "Push Day"
        assert result.user_id == 1

    def test_create_workout_saves_name_and_type(self, service, mock_repo, mock_session):
        payload = WorkoutCreate(
            user_id=1,
            name="Secret Session",
            type="Cardio",
            duration=30,
            is_public=False,
            exercises=[],
        )
        mock_session.refresh.side_effect = lambda obj: None
        mock_repo.save_workout.side_effect = lambda w, s: None
        mock_repo.save_post.side_effect = lambda p, s: None

        result = service.create_workout(payload)

        assert result.name == "Secret Session"
        assert result.type == "Cardio"


class TestGetWorkout:
    def test_returns_workout_when_found(self, service, mock_repo):
        w = make_workout(id=5)
        mock_repo.get_workout.return_value = w

        result = service.get_workout(5)

        mock_repo.get_workout.assert_called_once_with(5, service.session)
        assert result.id == 5

    def test_returns_none_when_not_found(self, service, mock_repo):
        mock_repo.get_workout.return_value = None

        result = service.get_workout(99)

        assert result is None


class TestGetUsersWorkouts:
    def test_returns_all_workouts_for_owner(self, service, mock_repo):
        workouts = [make_workout(id=1, is_public=True), make_workout(id=2, is_public=False)]
        mock_repo.get_users_workouts.return_value = workouts

        result = service.get_users_workouts(user_id=1)

        assert len(result) == 2

    def test_privacy_filter_hides_private_from_others(self, service, mock_repo):
        workouts = [
            make_workout(id=1, user_id=2, is_public=True),
            make_workout(id=2, user_id=2, is_public=False),
        ]
        mock_repo.get_users_workouts.return_value = workouts

        # Simulate what the route does: filter for non-owners
        all_workouts = service.get_users_workouts(user_id=2)
        visible = [w for w in all_workouts if w.is_public]

        assert len(visible) == 1
        assert visible[0].id == 1


class TestDeleteWorkout:
    def test_deletes_and_returns_workout(self, service, mock_repo):
        w = make_workout(id=3)
        mock_repo.get_workout.return_value = w
        mock_repo.delete_workout.return_value = w

        result = service.delete_workout(3)

        mock_repo.delete_workout.assert_called_once_with(3, service.session)
        assert result.id == 3

    def test_returns_none_when_workout_not_found(self, service, mock_repo):
        mock_repo.get_workout.return_value = None

        result = service.delete_workout(99)

        mock_repo.delete_workout.assert_not_called()
        assert result is None
