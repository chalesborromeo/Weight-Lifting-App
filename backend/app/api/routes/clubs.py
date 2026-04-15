from fastapi import Dependency, APIRouter

from app.services.club_service import ClubService

def get_club_service():
    return ClubService()

class ClubRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/clubs", tags=["clubs"])
        self.router.add_api_route("/", self.get_all, methods=["GET"])
        self.router.add_api_route("/user/{user_id}", self.create, methods=["POST"])
        self.router.add_apr_route("/{club_id}", self.get_one, methods=["GET"])

    # async def create(self, user_id: int, club: ClubCreate): # Need ClubCreate Pydantic Schema
    #     pass

    