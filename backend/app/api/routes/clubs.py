from fastapi import Depends, APIRouter

from app.services.club_service import ClubService
from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory

def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session

def get_club_service(session=Depends(get_db)) -> ClubService:
    repo = PostgreSQLFactory.create_db_repository()
    return ClubService(repo, session)

class ClubRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/clubs", tags=["clubs"])
        self.router.add_api_route("/", self.get_all, methods=["GET"])
        self.router.add_api_route("/user/{user_id}", self.create, methods=["POST"])
        self.router.add_apr_route("/{club_id}", self.get_one, methods=["GET"])

    

    # async def create(self, user_id: int, club: ClubCreate): # Need ClubCreate Pydantic Schema
    #     pass

    