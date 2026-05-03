"""
Basis Path Testing for Create Post Use Case

Control Flow Graph:
- D1: Text is provided?
- D2: Workout ID is provided?
- D3: Club ID is provided?

Paths:
1. Text only, no workout, no club (D1=True, D2=False, D3=False)
2. Text + workout, no club (D1=True, D2=True, D3=False)
3. Text + club, no workout (D1=True, D2=False, D3=True)
4. Text + workout + club (D1=True, D2=True, D3=True)
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostResponse
from app.models.post import Post
from app.models.user import User
from app.api.deps import get_db
from app.core.security import get_current_user_id
from app.api.routes.posts import get_post_service


class TestCreatePostBasisPaths:

    @pytest.fixture
    def mock_repo(self):
        return Mock()

    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def post_service(self, mock_repo, mock_session):
        return PostService(mock_repo, mock_session)

    @pytest.fixture
    def mock_user(self):
        user = User()
        user.id = 1
        user.email = "user@example.com"
        return user

    # PATH 1: Minimal post with text only
    def test_path1_minimal_post_text_only(self, post_service, mock_session):
        """
        Path 1: D1=True, D2=False, D3=False
        Scenario: Create a basic text-only post without workout or club context
        Expected: Post created with text set, workout_id and club_id are None
        """
        # Arrange
        user_id = 1
        post_data = PostCreate(
            text="Just had a great workout session!",
            workout_id=None,
            club_id=None
        )

        # Mock the session.refresh to populate post ID
        def refresh_post(post):
            post.id = 100

        mock_session.refresh.side_effect = refresh_post

        # Act
        result = post_service.create_post(user_id, post_data)

        # Assert
        assert result.user_id == user_id
        assert result.text == "Just had a great workout session!"
        assert result.workout_id is None
        assert result.club_id is None
        mock_session.refresh.assert_called_once()

    # PATH 2: Workout post with text and workout_id
    def test_path2_workout_post(self, post_service, mock_session):
        """
        Path 2: D1=True, D2=True, D3=False
        Scenario: Create a post tied to a specific workout session
        Expected: Post created with text and workout_id set, club_id is None
        """
        # Arrange
        user_id = 1
        post_data = PostCreate(
            text="Crushed my leg day!",
            workout_id=42,
            club_id=None
        )

        def refresh_post(post):
            post.id = 101

        mock_session.refresh.side_effect = refresh_post

        # Act
        result = post_service.create_post(user_id, post_data)

        # Assert
        assert result.user_id == user_id
        assert result.text == "Crushed my leg day!"
        assert result.workout_id == 42
        assert result.club_id is None
        mock_session.refresh.assert_called_once()

    # PATH 3: Club post with text and club_id
    def test_path3_club_post(self, post_service, mock_session):
        """
        Path 3: D1=True, D2=False, D3=True
        Scenario: Create a post for a specific gym club
        Expected: Post created with text and club_id set, workout_id is None
        """
        # Arrange
        user_id = 1
        post_data = PostCreate(
            text="Amazing workout with the crew!",
            workout_id=None,
            club_id=15
        )

        def refresh_post(post):
            post.id = 102

        mock_session.refresh.side_effect = refresh_post

        # Act
        result = post_service.create_post(user_id, post_data)

        # Assert
        assert result.user_id == user_id
        assert result.text == "Amazing workout with the crew!"
        assert result.workout_id is None
        assert result.club_id == 15
        mock_session.refresh.assert_called_once()

    # PATH 4: Full post with all fields
    def test_path4_full_post_all_fields(self, post_service, mock_session):
        """
        Path 4: D1=True, D2=True, D3=True
        Scenario: Create a post with all contextual information (text, workout, club)
        Expected: Post created with text, workout_id, and club_id all set
        """
        # Arrange
        user_id = 1
        post_data = PostCreate(
            text="Logged a new personal record!",
            workout_id=42,
            club_id=15
        )

        def refresh_post(post):
            post.id = 103

        mock_session.refresh.side_effect = refresh_post

        # Act
        result = post_service.create_post(user_id, post_data)

        # Assert
        assert result.user_id == user_id
        assert result.text == "Logged a new personal record!"
        assert result.workout_id == 42
        assert result.club_id == 15
        mock_session.refresh.assert_called_once()


# Integration test for the route endpoint
class TestCreatePostRouteEndpoint:

    def test_create_post_endpoint_success(self):
        """Integration test: Successful post creation through route endpoint"""
        from fastapi.testclient import TestClient
        from app.main import app
        from datetime import datetime, timezone

        # Arrange
        mock_user = User()
        mock_user.id = 1
        mock_user.email = "user@example.com"

        mock_post = Post()
        mock_post.id = 100
        mock_post.user_id = 1
        mock_post.user = mock_user
        mock_post.text = "Great workout!"
        mock_post.workout_id = 42
        mock_post.club_id = None
        mock_post.date = datetime.now(timezone.utc)
        mock_post.likes = 0

        def mock_get_post_service(session=None):
            service = Mock()
            service.create_post.return_value = mock_post
            return service

        def mock_get_current_user_id():
            return 1

        client = TestClient(app)

        # Override dependencies
        app.dependency_overrides[get_db] = lambda: Mock()
        app.dependency_overrides[get_current_user_id] = mock_get_current_user_id
        app.dependency_overrides[get_post_service] = mock_get_post_service

        # Act
        response = client.post(
            "/posts",
            json={
                "text": "Great workout!",
                "workout_id": 42,
                "club_id": None
            }
        )

        # Cleanup
        app.dependency_overrides.clear()

        # Assert
        assert response.status_code == 200  # FastAPI returns 200 for successful POST by default
        data = response.json()
        assert data["user_id"] == 1
        assert data["text"] == "Great workout!"
        assert data["workout_id"] == 42

    def test_create_post_endpoint_minimal(self):
        """Integration test: Create minimal post with only text"""
        from fastapi.testclient import TestClient
        from app.main import app
        from datetime import datetime, timezone

        # Arrange
        mock_user = User()
        mock_user.id = 1
        mock_user.email = "user@example.com"

        mock_post = Post()
        mock_post.id = 101
        mock_post.user_id = 1
        mock_post.user = mock_user
        mock_post.text = "Just had a great workout!"
        mock_post.workout_id = None
        mock_post.club_id = None
        mock_post.date = datetime.now(timezone.utc)
        mock_post.likes = 0

        def mock_get_post_service(session=None):
            service = Mock()
            service.create_post.return_value = mock_post
            return service

        def mock_get_current_user_id():
            return 1

        client = TestClient(app)

        # Override dependencies
        app.dependency_overrides[get_db] = lambda: Mock()
        app.dependency_overrides[get_current_user_id] = mock_get_current_user_id
        app.dependency_overrides[get_post_service] = mock_get_post_service

        # Act
        response = client.post(
            "/posts",
            json={"text": "Just had a great workout!"}
        )

        # Cleanup
        app.dependency_overrides.clear()

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "Just had a great workout!"
        assert data["workout_id"] is None
        assert data["club_id"] is None
