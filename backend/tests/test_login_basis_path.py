"""
Basis Path Testing for Login Use Case

Control Flow Graph:
- D1: User exists in database?
- D2: Password is correct?
- D3: Authentication result is truthy?

Paths:
1. User not found (D1=False)
2. User found, wrong password (D1=True, D2=False)
3. User found, correct password, auth returns falsy (D1=True, D2=True, D3=False)
4. Successful login (D1=True, D2=True, D3=True)
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from app.services.auth_service import AuthService
from app.schemas.auth import UserLogin, LoginResponse
from app.models.user import User


class TestLoginBasisPaths:

    @pytest.fixture
    def mock_repo(self):
        return Mock()

    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def auth_service(self, mock_repo, mock_session):
        return AuthService(mock_repo, mock_session)

    @pytest.fixture
    def valid_credentials(self):
        return UserLogin(email="user@example.com", password="password123")

    # PATH 1: User not found in database
    def test_path1_user_not_found(self, auth_service, mock_repo, valid_credentials):
        """
        Path 1: D1=False
        Scenario: Email does not exist in database
        Expected: authenticate_user returns False, login_user returns None
        """
        # Arrange
        mock_repo.get_user_by_email.return_value = None

        # Act
        result = auth_service.login_user(valid_credentials)

        # Assert
        mock_repo.get_user_by_email.assert_called_once_with("user@example.com", auth_service.session)
        assert result is None

    # PATH 2: User found but incorrect password
    @patch('app.services.auth_service.verify_password')
    def test_path2_wrong_password(self, mock_verify_password, auth_service, mock_repo, valid_credentials):
        """
        Path 2: D1=True, D2=False
        Scenario: User exists but password verification fails
        Expected: authenticate_user returns False, login_user returns None
        """
        # Arrange
        mock_user = User()
        mock_user.id = 1
        mock_user.email = "user@example.com"
        mock_user.password = "hashed_password"

        mock_repo.get_user_by_email.return_value = mock_user
        mock_verify_password.return_value = False

        # Act
        result = auth_service.login_user(valid_credentials)

        # Assert
        mock_repo.get_user_by_email.assert_called_once_with("user@example.com", auth_service.session)
        mock_verify_password.assert_called_once_with("password123", "hashed_password")
        assert result is None

    # PATH 3: User authenticated but returns falsy value
    @patch('app.services.auth_service.verify_password')
    def test_path3_authentication_returns_falsy(self, mock_verify_password, auth_service, mock_repo, valid_credentials):
        """
        Path 3: D1=True, D2=True, D3=False
        Scenario: User exists and password correct, but authenticate_user returns falsy
        Note: This path is technically redundant with paths 1 & 2, but included for complete basis set
        Expected: login_user returns None
        """
        # Arrange
        mock_user = User()
        mock_user.id = 1
        mock_user.email = "user@example.com"
        mock_user.password = "hashed_password"

        mock_repo.get_user_by_email.return_value = mock_user
        mock_verify_password.return_value = True

        # Simulate authenticate_user returning falsy by having it return False
        # This requires patching authenticate_user directly
        with patch.object(auth_service, 'authenticate_user', return_value=False):
            # Act
            result = auth_service.login_user(valid_credentials)

            # Assert
            assert result is None

    # PATH 4: Successful login
    @patch('app.services.auth_service.verify_password')
    @patch('app.services.auth_service.create_access_token')
    def test_path4_successful_login(self, mock_create_token, mock_verify_password, auth_service, mock_repo, valid_credentials):
        """
        Path 4: D1=True, D2=True, D3=True
        Scenario: User exists, password correct, authentication successful
        Expected: Returns LoginResponse with access token and user data
        """
        # Arrange
        mock_user = User()
        mock_user.id = 1
        mock_user.email = "user@example.com"
        mock_user.password = "hashed_password"

        mock_repo.get_user_by_email.return_value = mock_user
        mock_verify_password.return_value = True
        mock_create_token.return_value = "mock_jwt_token_12345"

        # Act
        result = auth_service.login_user(valid_credentials)

        # Assert
        mock_repo.get_user_by_email.assert_called_once_with("user@example.com", auth_service.session)
        mock_verify_password.assert_called_once_with("password123", "hashed_password")
        mock_create_token.assert_called_once_with({"sub": "1"})

        assert result is not None
        assert isinstance(result, LoginResponse)
        assert result.access_token == "mock_jwt_token_12345"
        assert result.token_type == "bearer"
        assert result.user == mock_user


# Integration test for the route endpoint
class TestLoginRouteEndpoint:

    @patch('app.api.routes.auth.get_auth_service')
    def test_login_endpoint_success(self, mock_get_service):
        """Integration test: Successful login through route endpoint"""
        from fastapi.testclient import TestClient
        from app.main import app

        # Arrange
        mock_service = Mock()
        mock_user = User()
        mock_user.id = 1
        mock_user.email = "user@example.com"

        mock_response = LoginResponse(
            access_token="test_token",
            token_type="bearer",
            user=mock_user
        )
        mock_service.login_user.return_value = mock_response
        mock_get_service.return_value = mock_service

        client = TestClient(app)

        # Act
        response = client.post(
            "/auth/login",
            json={"email": "user@example.com", "password": "password123"}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["access_token"] == "test_token"
        assert response.json()["token_type"] == "bearer"

    @patch('app.api.routes.auth.get_auth_service')
    def test_login_endpoint_invalid_credentials(self, mock_get_service):
        """Integration test: Invalid credentials return 401"""
        from fastapi.testclient import TestClient
        from app.main import app

        # Arrange
        mock_service = Mock()
        mock_service.login_user.return_value = None
        mock_get_service.return_value = mock_service

        client = TestClient(app)

        # Act
        response = client.post(
            "/auth/login",
            json={"email": "user@example.com", "password": "wrong_password"}
        )

        # Assert
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not Validate Credentials"
