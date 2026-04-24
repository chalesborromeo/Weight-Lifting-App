
from app.db.repositories import DBRepository
from app.models.user import User
from app.models.club import Club
from app.models.workout import Workout
from app.models.post import Post
from app.models.comment import Comment
from app.models.peer import Peer


class PostgreSQLRepository(DBRepository):

    def get_user_by_email(self, email, session):
        return session.query(User).filter(User.email == email).first()

    # User
    def get_all_users(self, session):
        return session.query(User).all()

    def save_user(self, user, session):
        session.add(user)
        session.flush()
        return user

    def get_user(self, user_id, session):
        return session.query(User).filter(User.id == user_id).first()

    # Club
    def get_all_clubs(self, session):
        return session.query(Club).all()
    
    def get_club(self, club_id, session):
        return session.query(Club).filter(Club.id == club_id).first()

    def save_club(self, club, session):
        session.add(club)
        session.flush()
        return club
    
    def delete_club(self, club_id, session):
        club = session.query(Club).filter(Club.id == club_id).first()
        if club:
            session.delete(club)
            session.flush()
    
    # Workout
    def get_all_workouts(self, session):
        return session.query(Workout).all()
    
    def get_users_workouts(self, user_id, session):
        return session.query(Workout).filter(Workout.user_id == user_id).all()
    
    def get_workout(self, workout_id, session):
        return session.query(Workout).filter(Workout.id == workout_id).first()

    def save_workout(self, workout, session):
        session.add(workout)
        session.flush()
        return workout
    
    def delete_workout(self, workout_id, session):
        workout = session.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            session.delete(workout)
            session.flush()

        return workout

    # Post
    def save_post(self, post, session):
        session.add(post)
        session.flush()
        return post

    def get_post(self, post_id, session):
        return session.query(Post).filter(Post.id == post_id).first()

    def get_feed_posts(self, user_ids, session):
        return (
            session.query(Post)
            .filter(Post.user_id.in_(user_ids))
            .order_by(Post.date.desc())
            .limit(50)
            .all()
        )

    def delete_post(self, post_id, session):
        post = session.query(Post).filter(Post.id == post_id).first()
        if post:
            session.delete(post)
            session.flush()
        return post

    # Comment
    def save_comment(self, comment, session):
        session.add(comment)
        session.flush()
        return comment

    def get_comments_for_post(self, post_id, session):
        return session.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.date.asc()).all()

    # Peer
    def save_peer(self, peer, session):
        session.add(peer)
        session.flush()
        return peer

    def get_peer(self, user_id, peer_id, session):
        return session.query(Peer).filter(
            Peer.user_id == user_id, Peer.peer_id == peer_id
        ).first()

    def get_peers_by_user(self, user_id, status, session):
        return session.query(Peer).filter(
            Peer.user_id == user_id, Peer.status == status
        ).all()

    def get_pending_for_user(self, user_id, session):
        return session.query(Peer).filter(
            Peer.peer_id == user_id, Peer.status == "pending"
        ).all()

    def delete_peer(self, peer_id, session):
        peer = session.query(Peer).filter(Peer.id == peer_id).first()
        if peer:
            session.delete(peer)
            session.flush()
        return peer

    def get_accepted_peer_ids(self, user_id, session):
        rows = session.query(Peer.peer_id).filter(
            Peer.user_id == user_id, Peer.status == "accepted"
        ).all()
        return [r[0] for r in rows]
