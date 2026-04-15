from fastapi import APIRouter, Depends

from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.db.postgresql.factory import PostgreSQLFactory

def get_user_service() -> UserService:
    return UserService(PostgreSQLFactory.create_db_repository())

class UserRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["users"])
        self.router.add_api_route("/", self.get_all, methods=["GET"])
        self.router.add_api_route("/register", self.create, methods=["POST"])
        self.router.add_api_route("/{user_id}", self.get_one, methods=["GET"])
        
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





