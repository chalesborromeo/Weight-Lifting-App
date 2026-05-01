from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.factory import PostgreSQLFactory
from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostResponse, CommentCreate, CommentResponse
from app.core.security import get_current_user_id
from app.api.deps import get_db


def get_post_service(session=Depends(get_db)) -> PostService:
    return PostService(PostgreSQLFactory.create_db_repository(), session)


class PostRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/posts", tags=["posts"])
        # NOTE: register concrete paths (e.g. /feed) BEFORE parameterised paths (e.g. /{post_id})
        # so FastAPI matches them first; otherwise /posts/feed gets routed to /posts/{post_id}.
        self.router.add_api_route("/feed", self.get_feed, methods=["GET"], response_model=List[PostResponse])
        self.router.add_api_route("/", self.create, methods=["POST"], response_model=PostResponse)
        self.router.add_api_route("/{post_id}", self.get_one, methods=["GET"], response_model=PostResponse)
        self.router.add_api_route("/{post_id}/like", self.like, methods=["POST"], response_model=PostResponse)
        self.router.add_api_route("/{post_id}/comments", self.add_comment, methods=["POST"], response_model=CommentResponse)
        self.router.add_api_route("/{post_id}/comments", self.get_comments, methods=["GET"], response_model=List[CommentResponse])
        self.router.add_api_route("/{post_id}", self.delete, methods=["DELETE"], response_model=PostResponse)

    async def get_feed(
        self,
        user_id: int = Depends(get_current_user_id),
        service: PostService = Depends(get_post_service),
    ):
        return service.get_feed(user_id)

    async def create(
        self,
        data: PostCreate,
        user_id: int = Depends(get_current_user_id),
        service: PostService = Depends(get_post_service),
    ):
        return service.create_post(user_id, data)

    async def get_one(self, post_id: int, service: PostService = Depends(get_post_service)):
        return service.get_post(post_id)

    async def like(
        self,
        post_id: int,
        _user_id: int = Depends(get_current_user_id),
        service: PostService = Depends(get_post_service),
    ):
        return service.like_post(post_id)

    async def add_comment(
        self,
        post_id: int,
        data: CommentCreate,
        user_id: int = Depends(get_current_user_id),
        service: PostService = Depends(get_post_service),
    ):
        return service.add_comment(post_id, user_id, data)

    async def get_comments(self, post_id: int, service: PostService = Depends(get_post_service)):
        return service.get_comments(post_id)

    async def delete(
        self,
        post_id: int,
        user_id: int = Depends(get_current_user_id),
        service: PostService = Depends(get_post_service),
    ):
        return service.delete_post(post_id, user_id)
