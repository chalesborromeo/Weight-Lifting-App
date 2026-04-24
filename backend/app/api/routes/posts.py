from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.post import PostCreate, PostResponse, PostUpdate, CommentCreate, CommentResponse
from app.services.post_service import PostService
from app.db.postgresql.factory import PostgreSQLFactory
from typing import List

from fastapi import APIRouter, Depends

from app.db.postgresql.factory import PostgreSQLFactory
from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostResponse, CommentCreate, CommentResponse
from app.core.security import get_current_user_id
from app.api.deps import get_db


def get_post_service(session=Depends(get_db)) -> PostService:
    return PostService(PostgreSQLFactory.create_db_repository(), session)
    repo = PostgreSQLFactory.create_db_repository()
    return PostService(repo, session)


class PostRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/posts", tags=["posts"])
        self.router.add_api_route("/", self.create, methods=["POST"], response_model=PostResponse)
        self.router.add_api_route("/", self.get_all, methods=["GET"], response_model=List[PostResponse])
        self.router.add_api_route("/{post_id}", self.get_one, methods=["GET"], response_model=PostResponse)
        self.router.add_api_route("/{post_id}", self.update, methods=["PUT"], response_model=PostResponse)
        self.router.add_api_route("/{post_id}", self.delete, methods=["DELETE"], response_model=PostResponse)
        self.router.add_api_route("/{post_id}/like", self.like, methods=["POST"], response_model=PostResponse)
        self.router.add_api_route("/{post_id}/unlike", self.unlike, methods=["POST"], response_model=PostResponse)
        self.router.add_api_route("/user/{user_id}", self.get_user_posts, methods=["GET"], response_model=List[PostResponse])
        self.router.add_api_route("/club/{club_id}", self.get_club_posts, methods=["GET"], response_model=List[PostResponse])
        
        # Comments
        self.router.add_api_route("/{post_id}/comments", self.create_comment, methods=["POST"], response_model=CommentResponse)
        self.router.add_api_route("/{post_id}/comments", self.get_comments, methods=["GET"], response_model=List[CommentResponse])
        self.router.add_api_route("/comments/{comment_id}", self.update_comment, methods=["PUT"], response_model=CommentResponse)
        self.router.add_api_route("/comments/{comment_id}", self.delete_comment, methods=["DELETE"], response_model=CommentResponse)

    async def create(self, post: PostCreate, service: PostService = Depends(get_post_service)):
        """Create a new post"""
        return service.create_post(post)

    async def get_all(self, service: PostService = Depends(get_post_service)):
        """Get all posts"""
        return service.get_all_posts()

    async def get_one(self, post_id: int, service: PostService = Depends(get_post_service)):
        """Get a specific post"""
        post = service.get_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def update(self, post_id: int, post_data: PostUpdate, service: PostService = Depends(get_post_service)):
        """Update a post"""
        post = service.update_post(post_id, post_data)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def delete(self, post_id: int, service: PostService = Depends(get_post_service)):
        """Delete a post"""
        post = service.delete_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def like(self, post_id: int, service: PostService = Depends(get_post_service)):
        """Like a post"""
        post = service.like_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def unlike(self, post_id: int, service: PostService = Depends(get_post_service)):
        """Unlike a post"""
        post = service.unlike_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def get_user_posts(self, user_id: int, service: PostService = Depends(get_post_service)):
        """Get all posts by a user"""
        return service.get_user_posts(user_id)

    async def get_club_posts(self, club_id: int, service: PostService = Depends(get_post_service)):
        """Get all posts in a club"""
        return service.get_club_posts(club_id)

    # Comments
    async def create_comment(self, post_id: int, comment: CommentCreate, service: PostService = Depends(get_post_service)):
        """Create a comment on a post"""
        return service.create_comment(comment)

    async def get_comments(self, post_id: int, service: PostService = Depends(get_post_service)):
        """Get all comments on a post"""
        return service.get_post_comments(post_id)

    async def update_comment(self, comment_id: int, text: str, service: PostService = Depends(get_post_service)):
        """Update a comment"""
        comment = service.update_comment(comment_id, text)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    async def delete_comment(self, comment_id: int, service: PostService = Depends(get_post_service)):
        """Delete a comment"""
        comment = service.delete_comment(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment
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

    async def like(self, post_id: int, service: PostService = Depends(get_post_service)):
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
