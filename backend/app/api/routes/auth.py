from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import TokenResponse, AuthResponse
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.db.postgresql.factory import PostgreSQLFactory
from app.db.postgresql.connection import PostgreSQLConnection


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


def get_auth_service(session=Depends(get_db)) -> AuthService:
    repo = PostgreSQLFactory.create_db_repository()
    return AuthService(repo, session)


def get_user_service(session=Depends(get_db)) -> UserService:
    repo = PostgreSQLFactory.create_db_repository()
    return UserService(repo, session)


class AuthRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.router.add_api_route("/register", self.register, methods=["POST"], response_model=UserResponse)
        self.router.add_api_route("/login", self.login, methods=["POST"], response_model=AuthResponse)

    async def register(self, user: UserCreate, service: UserService = Depends(get_user_service)):
        """
        Register a new user
        
        Args:
            user: User registration data (email, password)
            service: Injected UserService instance
            
        Returns:
            UserResponse: The newly created user
        """
        # Check if user already exists
        existing_user = None
        try:
            # This would need implementation in UserService
            existing_user = service.get_user_by_email(user.email)
        except:
            pass
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        new_user = service.create_user(user)
        return UserResponse.model_validate(new_user)

    async def login(self, credentials: UserLogin, service: AuthService = Depends(get_auth_service)):
        """
        Login user and return access token
        
        Args:
            credentials: User login credentials (email, password)
            service: Injected AuthService instance
            
        Returns:
            AuthResponse: Authentication token and user info
        """
        try:
            token_response = service.login(credentials)
            return AuthResponse(
                message="Login successful",
                token=token_response
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
