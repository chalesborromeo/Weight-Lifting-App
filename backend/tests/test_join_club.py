"""
Basis Path Testing for Join Club Use Case
 
Control Flow Graph:
- D1: Club exists in database?
- D2: User is already a member of the club?
- D3: Join is requested on behalf of self (member_id == user_id)?
 
Paths:
1. Club not found                          (D1=False)
2. Club found, user already a member      (D1=True, D2=True)
3. Successful join                         (D1=True, D2=False)
4. Route guard: joining on behalf of other (D3=False) → 403 before service is reached
"""
 
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
 
from app.services.club_service import ClubService
from app.models.club import Club
from app.models.user import User
 
 
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
 
def _make_user(user_id: int, email: str = None) -> User:
    u = User()
    u.id = user_id
    u.email = email or f"user{user_id}@example.com"
    u.password = "hashed"
    u.clubs = []
    u.owned_clubs = []
    u.posts = []
    u.comments = []
    u.notifications = []
    u.prs = []
    u.body_metrics = []
    u.favorite_exercises = []
    u.reports = []
    return u
 
 
def _make_club(club_id: int, owner_id: int, members: list = None) -> Club:
    c = Club()
    c.id = club_id
    c.name = "Power Lifters"
    c.description = "A club for serious lifters"
    c.privacy = "public"
    c.owner_id = owner_id
    c.owner = _make_user(owner_id)   # required for ClubResponse serialization
    c.members = members or []
    c.posts = []
    return c
 
 
# ---------------------------------------------------------------------------
# Service-layer unit tests
# ---------------------------------------------------------------------------
 
class TestJoinClubServiceBasisPaths:
 
    @pytest.fixture
    def mock_repo(self):
        return Mock()
 
    @pytest.fixture
    def mock_session(self):
        return Mock()
 
    @pytest.fixture
    def club_service(self, mock_repo, mock_session):
        return ClubService(mock_repo, mock_session)
 
    # PATH 1: Club not found
    def test_path1_club_not_found(self, club_service, mock_repo):
        """
        Path 1: D1=False
        Scenario: The requested club_id does not exist in the database.
        Expected: HTTPException 404 with 'Club not found'.
        """
        # Arrange
        user = _make_user(user_id=1)
        mock_repo.get_user.return_value = user
        mock_repo.get_club.return_value = None          # club missing
 
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            club_service.join_club(user_id=1, club_id=99)
 
        assert exc_info.value.status_code == 404
        assert "Club not found" in exc_info.value.detail
        mock_repo.get_club.assert_called_once_with(99, club_service.session)
 
    # PATH 2: User is already a member
    def test_path2_user_already_a_member(self, club_service, mock_repo):
        """
        Path 2: D1=True, D2=True
        Scenario: Club exists and the user is already listed as a member.
        Expected: HTTPException 400 with 'Already a member'.
        """
        # Arrange
        existing_member = _make_user(user_id=1)
        club = _make_club(club_id=10, owner_id=2, members=[existing_member])
 
        mock_repo.get_user.return_value = existing_member
        mock_repo.get_club.return_value = club
 
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            club_service.join_club(user_id=1, club_id=10)
 
        assert exc_info.value.status_code == 400
        assert "Already a member" in exc_info.value.detail
        # Repo should NOT persist anything
        mock_repo.save_club.assert_not_called()
 
    # PATH 3: Successful join
    def test_path3_successful_join(self, club_service, mock_repo):
        """
        Path 3: D1=True, D2=False
        Scenario: Club exists and the user is not yet a member.
        Expected: User is appended to club.members and club is persisted.
        """
        # Arrange
        new_member = _make_user(user_id=5)
        club = _make_club(club_id=10, owner_id=2, members=[])
 
        mock_repo.get_user.return_value = new_member
        mock_repo.get_club.return_value = club
        mock_repo.save_club.return_value = club
        club_service.session.refresh = Mock()           # prevent real DB call
 
        # Act
        result = club_service.join_club(user_id=5, club_id=10)
 
        # Assert
        assert new_member in club.members, "User should have been added to club.members"
        mock_repo.save_club.assert_called_once_with(club, club_service.session)
        club_service.session.refresh.assert_called_once_with(club)
        assert result is club
 
    # EDGE: Owner joining their own club (not already a member object)
    def test_owner_joins_as_member(self, club_service, mock_repo):
        """
        Edge case: The club owner calls join_club for themselves.
        The owner is not in club.members initially (owner relationship is separate).
        Expected: Owner is added to members list successfully.
        """
        # Arrange
        owner = _make_user(user_id=2)
        club = _make_club(club_id=10, owner_id=2, members=[])
 
        mock_repo.get_user.return_value = owner
        mock_repo.get_club.return_value = club
        mock_repo.save_club.return_value = club
        club_service.session.refresh = Mock()
 
        # Act
        result = club_service.join_club(user_id=2, club_id=10)
 
        # Assert
        assert owner in club.members
        mock_repo.save_club.assert_called_once()
        assert result is club
 
 
# ---------------------------------------------------------------------------
# Route-layer unit tests (enforces member_id == user_id guard)
# ---------------------------------------------------------------------------
 
class TestJoinClubRouteGuard:
    """
    Tests the HTTP route layer's identity check (PATH 4):
    a user cannot join a club on behalf of another user.
    """
 
    def test_path4_join_on_behalf_of_another_user_is_forbidden(self):
        """
        Path 4: D3=False
        Scenario: Authenticated user_id=1 tries to join as member_id=2.
        Expected: 403 Forbidden before the service layer is ever called.
        """
        from fastapi.testclient import TestClient
        from app.main import app
        from app.core.security import get_current_user_id
        from app.api.routes.clubs import get_club_service
 
        mock_service = Mock()
 
        app.dependency_overrides[get_current_user_id] = lambda: 1
        app.dependency_overrides[get_club_service] = lambda: mock_service
 
        client = TestClient(app)
 
        try:
            # Act: member_id in the path differs from the overridden user_id
            response = client.post("/clubs/10/member/2")
 
            # Assert
            assert response.status_code == 403
            assert "behalf of another user" in response.json()["detail"]
            mock_service.join_club.assert_not_called()
        finally:
            app.dependency_overrides.clear()
 
    def test_route_delegates_to_service_when_ids_match(self):
        """
        Scenario: member_id == user_id — route passes through to service.
        Expected: 200 OK and service.join_club is called once.
        """
        from fastapi.testclient import TestClient
        from app.main import app
        from app.core.security import get_current_user_id
        from app.api.routes.clubs import get_club_service
 
        user = _make_user(user_id=1)
        club = _make_club(club_id=10, owner_id=2, members=[user])
 
        mock_service = Mock()
        mock_service.join_club.return_value = club
 
        app.dependency_overrides[get_current_user_id] = lambda: 1
        app.dependency_overrides[get_club_service] = lambda: mock_service
 
        client = TestClient(app)
 
        try:
            # Act: member_id == user_id == 1
            response = client.post("/clubs/10/member/1")
 
            # Assert
            assert response.status_code == 200
            mock_service.join_club.assert_called_once_with(1, 10)
        finally:
            app.dependency_overrides.clear()