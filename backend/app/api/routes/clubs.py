from typing import List

from fastapi import Depends, APIRouter
from pydantic import BaseModel

from app.services.club_service import ClubService
from app.db.postgresql.factory import PostgreSQLFactory
from app.schemas.club import ClubCreate, ClubResponse
from app.schemas.post import PostResponse
from app.core.security import get_current_user_id
from app.api.deps import get_db


class ClubPostCreate(BaseModel):
    text: str

def get_club_service(session=Depends(get_db)) -> ClubService:
    repo = PostgreSQLFactory.create_db_repository()
    return ClubService(repo, session)

class ClubRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/clubs", tags=["clubs"])
        self.router.add_api_route("/", self.get_all, methods=["GET"], response_model=List[ClubResponse])
        self.router.add_api_route("/", self.create, methods=["POST"], response_model=ClubResponse)
        self.router.add_api_route("/{club_id}", self.get_one, methods=["GET"], response_model=ClubResponse)
        self.router.add_api_route("/{club_id}", self.delete, methods=["DELETE"], response_model=ClubResponse)
        self.router.add_api_route("/{club_id}/member/{member_id}", self.join, methods=["POST"], response_model=ClubResponse)
        self.router.add_api_route("/{club_id}/member/{member_id}", self.leave, methods=["DELETE"], response_model=ClubResponse)
        self.router.add_api_route("/{club_id}/feed", self.get_feed, methods=["GET"], response_model=List[PostResponse])
        self.router.add_api_route("/{club_id}/posts", self.create_post, methods=["POST"], response_model=PostResponse)

    async def get_all(self, service: ClubService = Depends(get_club_service)):
        return service.get_all_clubs()

    async def create(self, club: ClubCreate, service: ClubService = Depends(get_club_service)):
        return service.create_club(club)
    
    async def get_one(self, club_id:int, service: ClubService = Depends(get_club_service)):
        return service.get_club(club_id)
    
    async def delete(self, club_id:int, service: ClubService = Depends(get_club_service)):
        return service.delete_club(club_id)
    
    async def join(self, club_id:int, member_id:int, service: ClubService = Depends(get_club_service)):
        return service.join_club(member_id, club_id)
    
    async def leave(self, club_id:int, member_id:int, service: ClubService = Depends(get_club_service)):
        return service.leave_club(member_id, club_id)

    async def get_feed(self, club_id: int, service: ClubService = Depends(get_club_service)):
        return service.get_club_feed(club_id)

    async def create_post(
        self,
        club_id: int,
        data: ClubPostCreate,
        user_id: int = Depends(get_current_user_id),
        service: ClubService = Depends(get_club_service),
    ):
        return service.create_club_post(club_id, user_id, data.text)
