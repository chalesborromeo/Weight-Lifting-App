from fastapi import APIRouter, Depends

from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.db.postgresql.factory import PostgreSQLFactory
from app.db.postgresql.connection import PostgreSQLConnection
from app.schemas.user import UserResponse

def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session

def get_user_service(session = Depends(get_db)) -> UserService:
    repo = PostgreSQLFactory.create_db_repository()
    return UserService(repo, session)

class UserRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["users"])
        self.router.add_api_route("/", self.get_all, methods=["GET"], response_model=list[UserResponse])
        self.router.add_api_route("/register", self.create, methods=["POST"], response_model=UserResponse)
        self.router.add_api_route("/search", self.search, methods=["GET"], response_model=list[UserResponse])
        self.router.add_api_route("/{user_id}", self.get_one, methods=["GET"], response_model=UserResponse)

    async def get_all(self, service:UserService = Depends(get_user_service)):
        """
        Retrieve all users

        Args:
            service (UserService): Injected UserService instance.
        
        Returns:
            list: A list of all users
        """
        return service.get_all_users()

    async def create(self, user: UserCreate, service:UserService = Depends(get_user_service)):
        """
        Registers a new user

        Args:
            service (UserService): Injected UserService instance

        Returns:
            User: The newly created user 
        """
        return service.create_user(user)

    async def search(self, q: str, service:UserService = Depends(get_user_service)):
        """
        Search users by email substring (SRS 3.1.26 Search Peer).
        """
        return service.search_users(q)

    async def get_one(self, user_id: int, service:UserService = Depends(get_user_service)):
        """
        Retrieves a single user by id.

        Args:
            user_id(int): Unique identifier of the user, extracted from request path
            service(UserService): Injected UserService instance
        
        Returns:
            User: The user record matching the given user_id
        """
        return service.get_user(user_id)





