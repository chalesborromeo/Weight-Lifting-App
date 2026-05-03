"""
Unit tests for Gym Check-in use cases (SRS 3.1.29)
- 3.1.29 Gym Check-in
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from fastapi import HTTPException

from app.services.gym_service import GymService
from app.schemas.gym import GymCheckInCreate
from app.models.gym_checkin import GymCheckIn


def make_checkin(id=1, user_id=1, gym_name="Planet Fitness", gym_address="123 Main St"):
    c = GymCheckIn()
    c.id = id
    c.user_id = user_id
    c.gym_name = gym_name
    c.gym_address = gym_address
    c.checked_in_at = datetime.now()
    return c


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def mock_session():
    return Mock()


@pytest.fixture
def service(mock_repo, mock_session):
    return GymService(mock_repo, mock_session)


class TestGymCheckIn:
    def test_creates_checkin(self, service, mock_repo, mock_session):
        data = GymCheckInCreate(gym_name="Planet Fitness", gym_address="123 Main St")
        mock_session.refresh.side_effect = lambda obj: None

        def fake_save(checkin, session):
            checkin.id = 1
            checkin.checked_in_at = datetime.now()
        mock_repo.save_checkin.side_effect = fake_save

        result = service.checkin(user_id=1, data=data)

        mock_repo.save_checkin.assert_called_once()
        assert result.gym_name == "Planet Fitness"
        assert result.user_id == 1

    def test_checkin_without_address(self, service, mock_repo, mock_session):
        data = GymCheckInCreate(gym_name="Local Gym")
        mock_session.refresh.side_effect = lambda obj: None
        mock_repo.save_checkin.side_effect = lambda c, s: None

        result = service.checkin(user_id=1, data=data)

        assert result.gym_address is None


class TestListCheckIns:
    def test_returns_checkins_for_user(self, service, mock_repo):
        checkins = [
            make_checkin(id=1, gym_name="Planet Fitness"),
            make_checkin(id=2, gym_name="Gold's Gym"),
        ]
        mock_repo.get_checkins_by_user.return_value = checkins

        result = service.list_checkins(user_id=1)

        mock_repo.get_checkins_by_user.assert_called_once_with(1, service.session)
        assert len(result) == 2
        assert result[0].gym_name == "Planet Fitness"

    def test_returns_empty_list_when_no_checkins(self, service, mock_repo):
        mock_repo.get_checkins_by_user.return_value = []

        result = service.list_checkins(user_id=1)

        assert result == []


class TestDeleteCheckIn:
    def test_deletes_own_checkin(self, service, mock_repo):
        checkin = make_checkin(id=3, user_id=1)
        mock_repo.delete_checkin.return_value = checkin

        result = service.delete_checkin(checkin_id=3, user_id=1)

        mock_repo.delete_checkin.assert_called_once_with(3, 1, service.session)
        assert result.id == 3

    def test_raises_404_when_not_found(self, service, mock_repo):
        mock_repo.delete_checkin.return_value = None

        with pytest.raises(HTTPException) as exc:
            service.delete_checkin(checkin_id=99, user_id=1)

        assert exc.value.status_code == 404
