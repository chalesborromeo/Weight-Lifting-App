"""
Unit tests for Post use cases (SRS 3.1.8, 3.1.9, 3.1.11, 3.1.12, 3.1.13, 3.1.14)
- 3.1.8  View Feed
- 3.1.9  Create Post
- 3.1.11 Delete Post
- 3.1.12 Like Post
- 3.1.13 Comment on Post
- 3.1.14 Edit Post
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from fastapi import HTTPException

from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostUpdate, CommentCreate
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User


def make_user(id=1, email="user@test.com"):
    u = User()
    u.id = id
    u.email = email
    return u


def make_post(id=1, user_id=1, text="Great workout today!", likes=0):
    p = Post()
    p.id = id
    p.user_id = user_id
    p.text = text
    p.likes = likes
    p.date = datetime.now()
    p.comments = []
    p.user = make_user(user_id)
    return p


def make_comment(id=1, post_id=1, user_id=1, text="Nice!"):
    c = Comment()
    c.id = id
    c.post_id = post_id
    c.user_id = user_id
    c.text = text
    c.date = datetime.now()
    c.user = make_user(user_id)
    return c


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def mock_session():
    return Mock()


@pytest.fixture
def service(mock_repo, mock_session):
    return PostService(mock_repo, mock_session)


class TestCreatePost:
    def test_creates_post_with_text(self, service, mock_repo, mock_session):
        payload = PostCreate(text="Just hit a new PR!")
        created = make_post(text="Just hit a new PR!")
        mock_session.refresh.side_effect = lambda obj: None

        def fake_save(post, session):
            post.id = 1
        mock_repo.save_post.side_effect = fake_save

        result = service.create_post(user_id=1, data=payload)

        mock_repo.save_post.assert_called_once()
        assert result.text == "Just hit a new PR!"
        assert result.user_id == 1

    def test_creates_post_with_workout(self, service, mock_repo, mock_session):
        payload = PostCreate(workout_id=5)
        mock_session.refresh.side_effect = lambda obj: None
        mock_repo.save_post.side_effect = lambda p, s: None

        result = service.create_post(user_id=1, data=payload)

        assert result.workout_id == 5


class TestGetFeed:
    def test_returns_posts_from_peers(self, service, mock_repo):
        mock_repo.get_accepted_peer_ids.return_value = [2, 3]
        posts = [make_post(id=1, user_id=1), make_post(id=2, user_id=2)]
        mock_repo.get_feed_posts.return_value = posts

        result = service.get_feed(user_id=1)

        # Feed includes self + accepted peers
        mock_repo.get_feed_posts.assert_called_once()
        assert len(result) == 2

    def test_feed_falls_back_to_public_when_empty(self, service, mock_repo):
        mock_repo.get_accepted_peer_ids.return_value = []
        mock_repo.get_feed_posts.return_value = []
        fallback = [make_post(id=10, user_id=5)]
        mock_repo.get_all_posts.return_value = fallback

        result = service.get_feed(user_id=1)

        assert len(result) == 1
        assert result[0].id == 10


class TestLikePost:
    def test_increments_likes(self, service, mock_repo, mock_session):
        post = make_post(id=1, likes=3)
        mock_repo.get_post.return_value = post
        mock_session.flush.return_value = None
        mock_session.refresh.side_effect = lambda obj: None

        result = service.like_post(1)

        assert result.likes == 4

    def test_raises_404_when_post_not_found(self, service, mock_repo):
        mock_repo.get_post.return_value = None

        with pytest.raises(HTTPException) as exc:
            service.like_post(99)

        assert exc.value.status_code == 404


class TestAddComment:
    def test_adds_comment_to_post(self, service, mock_repo, mock_session):
        post = make_post(id=1)
        mock_repo.get_post.return_value = post
        comment = make_comment(text="Keep it up!")
        mock_session.refresh.side_effect = lambda obj: None

        def fake_save(c, session):
            c.id = 1
        mock_repo.save_comment.side_effect = fake_save

        result = service.add_comment(post_id=1, user_id=1, data=CommentCreate(text="Keep it up!"))

        mock_repo.save_comment.assert_called_once()
        assert result.text == "Keep it up!"

    def test_raises_404_on_missing_post(self, service, mock_repo):
        mock_repo.get_post.return_value = None

        with pytest.raises(HTTPException) as exc:
            service.add_comment(post_id=99, user_id=1, data=CommentCreate(text="Hi"))

        assert exc.value.status_code == 404


class TestEditPost:
    def test_owner_can_edit_text(self, service, mock_repo, mock_session):
        post = make_post(id=1, user_id=1, text="Old text")
        mock_repo.get_post.return_value = post
        mock_session.flush.return_value = None
        mock_session.refresh.side_effect = lambda obj: None

        result = service.update_post(post_id=1, user_id=1, data=PostUpdate(text="New text"))

        assert result.text == "New text"

    def test_non_owner_cannot_edit(self, service, mock_repo):
        post = make_post(id=1, user_id=2)
        mock_repo.get_post.return_value = post

        with pytest.raises(HTTPException) as exc:
            service.update_post(post_id=1, user_id=1, data=PostUpdate(text="Hacked"))

        assert exc.value.status_code == 403

    def test_raises_404_when_post_not_found(self, service, mock_repo):
        mock_repo.get_post.return_value = None

        with pytest.raises(HTTPException) as exc:
            service.update_post(post_id=99, user_id=1, data=PostUpdate(text="x"))

        assert exc.value.status_code == 404


class TestDeletePost:
    def test_owner_can_delete(self, service, mock_repo):
        post = make_post(id=1, user_id=1)
        mock_repo.get_post.return_value = post

        result = service.delete_post(post_id=1, user_id=1)

        mock_repo.delete_post.assert_called_once_with(1, service.session)
        assert result.id == 1

    def test_non_owner_cannot_delete(self, service, mock_repo):
        post = make_post(id=1, user_id=2)
        mock_repo.get_post.return_value = post

        with pytest.raises(HTTPException) as exc:
            service.delete_post(post_id=1, user_id=1)

        assert exc.value.status_code == 403
