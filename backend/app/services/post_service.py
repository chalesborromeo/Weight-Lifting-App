from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.models.post import Post
from app.models.comment import Comment
from app.schemas.post import PostCreate, PostUpdate, CommentCreate


class PostService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def create_post(self, user_id: int, data: PostCreate):
        post = Post()
        post.user_id = user_id
        post.text = data.text
        post.workout_id = data.workout_id
        post.club_id = data.club_id
        self.repo.save_post(post, self.session)
        self.session.refresh(post)
        return post

    def create_post_for_workout(self, user_id: int, workout_id: int, workout_name: str):
        post = Post()
        post.user_id = user_id
        post.workout_id = workout_id
        post.text = f"Just completed {workout_name} 💪"
        self.repo.save_post(post, self.session)
        self.session.refresh(post)
        return post

    def get_feed(self, user_id: int):
        peer_ids = self.repo.get_accepted_peer_ids(user_id, self.session)
        if not peer_ids:
            return self.repo.get_all_posts(self.session)
        feed_user_ids = [user_id] + peer_ids
        return self.repo.get_feed_posts(feed_user_ids, self.session)
    
    def get_all_posts(self):
        return self.repo.get_all_posts(self.session)


    def get_post(self, post_id: int):
        post = self.repo.get_post(post_id, self.session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post

    def like_post(self, post_id: int):
        post = self.repo.get_post(post_id, self.session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        post.likes += 1
        self.session.flush()
        self.session.refresh(post)
        return post

    def add_comment(self, post_id: int, user_id: int, data: CommentCreate):
        post = self.repo.get_post(post_id, self.session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        comment = Comment()
        comment.post_id = post_id
        comment.user_id = user_id
        comment.text = data.text
        self.repo.save_comment(comment, self.session)
        self.session.refresh(comment)
        return comment

    def get_comments(self, post_id: int):
        return self.repo.get_comments_for_post(post_id, self.session)

    def update_post(self, post_id: int, user_id: int, data: PostUpdate):
        post = self.repo.get_post(post_id, self.session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot edit another user's post")
        if data.text is not None:
            post.text = data.text
        self.session.flush()
        self.session.refresh(post)
        return post

    def delete_post(self, post_id: int, user_id: int):
        post = self.repo.get_post(post_id, self.session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete another user's post")
        self.repo.delete_post(post_id, self.session)
        return post
