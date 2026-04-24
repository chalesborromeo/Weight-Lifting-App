from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.repositories import DBRepository
from app.models.post import Post
from app.models.comment import Comment
from app.schemas.post import PostCreate, PostResponse, CommentCreate, CommentResponse, PostUpdate


class PostService:
    def __init__(self, repo: DBRepository, session: Session):
        self.repo = repo
        self.session = session

    def get_all_posts(self) -> List[Post]:
        """Get all posts"""
        stmt = select(Post)
        posts = self.session.execute(stmt).scalars().all()
        return posts

    def get_post(self, post_id: int) -> Optional[Post]:
        """Get a post by ID"""
        stmt = select(Post).where(Post.id == post_id)
        post = self.session.execute(stmt).scalars().first()
        return post

    def get_user_posts(self, user_id: int) -> List[Post]:
        """Get all posts by a user"""
        stmt = select(Post).where(Post.user_id == user_id)
        posts = self.session.execute(stmt).scalars().all()
        return posts

    def get_club_posts(self, club_id: int) -> List[Post]:
        """Get all posts in a club"""
        stmt = select(Post).where(Post.club_id == club_id)
        posts = self.session.execute(stmt).scalars().all()
        return posts

    def create_post(self, post_data: PostCreate) -> Post:
        """Create a new post"""
        new_post = Post(
            user_id=post_data.user_id,
            text=post_data.text,
            workout_id=post_data.workout_id,
            club_id=post_data.club_id
        )
        
        self.session.add(new_post)
        self.session.commit()
        self.session.refresh(new_post)
        return new_post

    def update_post(self, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        """Update a post"""
        post = self.get_post(post_id)
        if not post:
            return None
        
        if post_data.text is not None:
            post.text = post_data.text
        
        if post_data.likes is not None:
            post.likes = post_data.likes
        
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete_post(self, post_id: int) -> Optional[Post]:
        """Delete a post"""
        post = self.get_post(post_id)
        if not post:
            return None
        
        self.session.delete(post)
        self.session.commit()
        return post

    def like_post(self, post_id: int) -> Optional[Post]:
        """Increment likes on a post"""
        post = self.get_post(post_id)
        if not post:
            return None
        
        post.likes += 1
        self.session.commit()
        self.session.refresh(post)
        return post

    def unlike_post(self, post_id: int) -> Optional[Post]:
        """Decrement likes on a post"""
        post = self.get_post(post_id)
        if not post:
            return None
        
        if post.likes > 0:
            post.likes -= 1
        
        self.session.commit()
        self.session.refresh(post)
        return post

    # Comment operations
    def create_comment(self, comment_data: CommentCreate) -> Comment:
        """Create a new comment on a post"""
        new_comment = Comment(
            user_id=comment_data.user_id,
            post_id=comment_data.post_id,
            text=comment_data.text
        )
        
        self.session.add(new_comment)
        self.session.commit()
        self.session.refresh(new_comment)
        return new_comment

    def get_comment(self, comment_id: int) -> Optional[Comment]:
        """Get a comment by ID"""
        stmt = select(Comment).where(Comment.id == comment_id)
        comment = self.session.execute(stmt).scalars().first()
        return comment

    def get_post_comments(self, post_id: int) -> List[Comment]:
        """Get all comments on a post"""
        stmt = select(Comment).where(Comment.post_id == post_id)
        comments = self.session.execute(stmt).scalars().all()
        return comments

    def delete_comment(self, comment_id: int) -> Optional[Comment]:
        """Delete a comment"""
        comment = self.get_comment(comment_id)
        if not comment:
            return None
        
        self.session.delete(comment)
        self.session.commit()
        return comment

    def update_comment(self, comment_id: int, text: str) -> Optional[Comment]:
        """Update a comment"""
        comment = self.get_comment(comment_id)
        if not comment:
            return None
        
        comment.text = text
        self.session.commit()
        self.session.refresh(comment)
        return comment
