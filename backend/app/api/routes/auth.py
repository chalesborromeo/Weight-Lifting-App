from fastapi import Depends, APIRouter, HTTPException

from app.db.postgresql.factory import PostgreSQLFactory
from app.db.postgresql.connection import PostgreSQLConnection
from app.services.auth_service import AuthService
from app.schemas.auth import LoginResponse, UserLogin, UserRegister

def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session

def get_auth_service(session = Depends(get_db)):
    repo = PostgreSQLFactory.create_db_repository()
    return AuthService(repo, session)

class AuthRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.router.add_api_route("/login", self.login, methods=["POST"], response_model=LoginResponse)
        self.router.add_api_route("/register", self.register, methods=["POST"], response_model=LoginResponse)
        self.router.add_api_route("/logout", self.logout, methods=["POST"])
        self.router.add_api_route("/refresh", self.refresh, methods=["POST"])

    async def login(self, credentials: UserLogin, service: AuthService = Depends(get_auth_service)):
        result = service.login_user(credentials)
        if not result:
            raise HTTPException(status_code=401, detail="Could not Validate Credentials")
        
        return result

    async def register(self, user:UserRegister, service: AuthService = Depends(get_auth_service)):
        return service.register_user(user)

    async def logout(self):
        return {"message": "Logged out"}

    async def refresh(self):
        raise HTTPException(status_code=501, detail="Not implemented")

