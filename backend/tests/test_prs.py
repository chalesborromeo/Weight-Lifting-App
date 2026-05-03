"""
Unit tests for Personal Records use cases (SRS 3.1.16, 3.1.17, 3.1.18, 3.1.30)
- 3.1.16 Track Personal Records
- 3.1.17 View Personal Records
- 3.1.18 Share PR to Feed
- 3.1.30 Leaderboard
"""

import pytest
from unittest.mock import Mock
from datetime import date
from fastapi import HTTPException

from app.services.pr_service import PRService
from app.schemas.pr import PRCreate
from app.models.pr import PR
from app.models.user import User


def make_pr(id=1, user_id=1, exercise="Bench Press", weight=225.0, reps=5):
    pr = PR()
    pr.id = id
    pr.user_id = user_id
    pr.exercise_name = exercise
    pr.weight = weight
    pr.reps = reps
    pr.date = date.today()
    pr.user = make_user(user_id)
    return pr


def make_user(id=1, email="user@test.com"):
    u = User()
    u.id = id
    u.email = email
    return u


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def mock_session():
    return Mock()


@pytest.fixture
def service(mock_repo, mock_session):
    return PRService(mock_repo, mock_session)


class TestCreatePR:
    def test_creates_and_returns_pr(self, service, mock_repo, mock_session):
        payload = PRCreate(exercise_name="Squat", weight=315.0, reps=3)
        mock_session.refresh.side_effect = lambda obj: None

        def fake_save(pr, session):
            pr.id = 1
            pr.date = date.today()
        mock_repo.save_pr.side_effect = fake_save

        result = service.create_pr(user_id=1, data=payload)

        mock_repo.save_pr.assert_called_once()
        assert result.exercise_name == "Squat"
        assert result.weight == 315.0
        assert result.user_id == 1

    def test_pr_stores_correct_reps(self, service, mock_repo, mock_session):
        payload = PRCreate(exercise_name="Deadlift", weight=405.0, reps=1)
        mock_session.refresh.side_effect = lambda obj: None
        mock_repo.save_pr.side_effect = lambda pr, s: None

        result = service.create_pr(user_id=2, data=payload)

        assert result.reps == 1


class TestListPRs:
    def test_returns_users_prs(self, service, mock_repo):
        prs = [make_pr(id=1), make_pr(id=2, exercise="Squat")]
        mock_repo.get_prs_by_user.return_value = prs

        result = service.list_prs(user_id=1)

        mock_repo.get_prs_by_user.assert_called_once_with(1, service.session)
        assert len(result) == 2

    def test_returns_empty_list_when_no_prs(self, service, mock_repo):
        mock_repo.get_prs_by_user.return_value = []

        result = service.list_prs(user_id=1)

        assert result == []


class TestDeletePR:
    def test_deletes_own_pr(self, service, mock_repo):
        pr = make_pr(id=5, user_id=1)
        mock_repo.get_pr.return_value = pr

        result = service.delete_pr(user_id=1, pr_id=5)

        mock_repo.delete_pr.assert_called_once_with(5, service.session)
        assert result == {"message": "PR deleted"}

    def test_raises_403_deleting_others_pr(self, service, mock_repo):
        pr = make_pr(id=5, user_id=2)
        mock_repo.get_pr.return_value = pr

        with pytest.raises(HTTPException) as exc:
            service.delete_pr(user_id=1, pr_id=5)

        assert exc.value.status_code == 403

    def test_raises_404_when_pr_not_found(self, service, mock_repo):
        mock_repo.get_pr.return_value = None

        with pytest.raises(HTTPException) as exc:
            service.delete_pr(user_id=1, pr_id=99)

        assert exc.value.status_code == 404


class TestLeaderboard:
    def test_returns_sorted_top_prs(self, service, mock_repo):
        top = [
            make_pr(id=1, user_id=1, weight=315.0),
            make_pr(id=2, user_id=2, weight=275.0),
        ]
        mock_repo.get_top_prs_by_exercise.return_value = top

        result = service.leaderboard("Squat", limit=10)

        mock_repo.get_top_prs_by_exercise.assert_called_once_with("Squat", 10, service.session)
        assert len(result) == 2
        assert result[0].weight == 315.0


class TestSharePRToFeed:
    """
    3.1.18 — sharing a PR creates a post via postsApi.create on the frontend.
    Backend test: verify POST /posts/ with a PR-style text succeeds.
    """

    def test_share_pr_creates_post(self, client):
        from app.main import app
        from app.api.routes.posts import get_post_service
        from app.api.routes.auth import get_auth_service
        from app.core.security import get_current_user_id
        from app.models.post import Post
        from datetime import datetime

        mock_post = Post()
        mock_post.id = 1
        mock_post.user_id = 1
        mock_post.text = "🏆 New PR! Bench Press — 225 lbs × 5 reps"
        mock_post.likes = 0
        mock_post.date = datetime.now()
        mock_post.comments = []
        mock_post.user = make_user()

        mock_post_service = Mock()
        mock_post_service.create_post.return_value = mock_post

        app.dependency_overrides[get_post_service] = lambda: mock_post_service
        app.dependency_overrides[get_current_user_id] = lambda: 1

        from fastapi.testclient import TestClient
        c = TestClient(app)
        response = c.post("/posts/", json={"text": "🏆 New PR! Bench Press — 225 lbs × 5 reps"})

        app.dependency_overrides.clear()

        assert response.status_code == 200
        assert "PR" in response.json()["text"]
