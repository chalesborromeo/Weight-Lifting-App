from sqlalchemy import or_, desc

from app.db.repositories import DBRepository
from app.models.user import User
from app.models.club import Club
from app.models.workout import Workout
from app.models.post import Post
from app.models.comment import Comment
from app.models.peer import Peer
from app.models.profile import Profile
from app.models.pr import PR
from app.models.gym import Gym
from app.models.body_metric import BodyMetric
from app.models.favorite_exercise import FavoriteExercise
from app.models.report import Report
from app.models.notification import Notification
from app.models.spot_Request import Spot_Request


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

    def get_user_suggestions(self, user_id, session):
        sent_ids = [r[0] for r in session.query(Peer.peer_id).filter(Peer.user_id == user_id)]
        received_ids = [r[0] for r in session.query(Peer.user_id).filter(Peer.peer_id == user_id)]
        exclude = set([user_id] + sent_ids + received_ids)
        return (
            session.query(User)
            .filter(~User.id.in_(exclude))
            .order_by(User.id.desc())
            .limit(8)
            .all()
        )

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

    def get_club_posts(self, club_id, session):
        return (
            session.query(Post)
            .filter(Post.club_id == club_id)
            .order_by(Post.date.desc())
            .limit(50)
            .all()
        )

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

    def get_all_posts(self, session):
        return (
            session.query(Post)
            .order_by(Post.date.desc())
            .limit(50)
            .all()
        )

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

    # Profile
    def get_profile_by_user(self, user_id, session):
        return session.query(Profile).filter(Profile.user_id == user_id).first()

    def save_profile(self, profile, session):
        session.add(profile)
        session.flush()
        return profile

    # User search — matches email (only searchable field on User right now)
    def search_users(self, query, session):
        pattern = f"%{query}%"
        return session.query(User).filter(User.email.ilike(pattern)).limit(50).all()

    # PR
    def save_pr(self, pr, session):
        session.add(pr)
        session.flush()
        return pr

    def get_prs_by_user(self, user_id, session):
        return (
            session.query(PR)
            .filter(PR.user_id == user_id)
            .order_by(PR.date.desc())
            .all()
        )

    def get_pr(self, pr_id, session):
        return session.query(PR).filter(PR.id == pr_id).first()

    def delete_pr(self, pr_id, session):
        pr = session.query(PR).filter(PR.id == pr_id).first()
        if pr:
            session.delete(pr)
            session.flush()
        return pr

    def get_top_prs_by_exercise(self, exercise_name, limit, session):
        return (
            session.query(PR)
            .filter(PR.exercise_name == exercise_name)
            .order_by(PR.weight.desc())
            .limit(limit)
            .all()
        )

    # Gym
    def get_all_gyms(self, session):
        return session.query(Gym).all()

    def get_gym(self, gym_id, session):
        return session.query(Gym).filter(Gym.id == gym_id).first()

    def save_gym(self, gym, session):
        session.add(gym)
        session.flush()
        return gym

    # BodyMetric
    def save_body_metric(self, metric, session):
        session.add(metric)
        session.flush()
        return metric

    def get_body_metrics_by_user(self, user_id, session):
        return (
            session.query(BodyMetric)
            .filter(BodyMetric.user_id == user_id)
            .order_by(BodyMetric.date.desc())
            .all()
        )

    # FavoriteExercise
    def save_favorite_exercise(self, favorite, session):
        session.add(favorite)
        session.flush()
        return favorite

    def get_favorite_exercises_by_user(self, user_id, session):
        return (
            session.query(FavoriteExercise)
            .filter(FavoriteExercise.user_id == user_id)
            .order_by(FavoriteExercise.name.asc())
            .all()
        )

    def get_favorite_exercise(self, favorite_id, session):
        return session.query(FavoriteExercise).filter(FavoriteExercise.id == favorite_id).first()

    def delete_favorite_exercise(self, favorite_id, session):
        favorite = session.query(FavoriteExercise).filter(FavoriteExercise.id == favorite_id).first()
        if favorite:
            session.delete(favorite)
            session.flush()
        return favorite

    # Report
    def save_report(self, report, session):
        session.add(report)
        session.flush()
        return report

    def get_reports_for_post(self, post_id, session):
        return (
            session.query(Report)
            .filter(Report.post_id == post_id)
            .order_by(Report.created_at.desc())
            .all()
        )

    def get_unresolved_reports(self, session):
        return (
            session.query(Report)
            .filter(Report.resolved == False)  # noqa: E712
            .order_by(Report.created_at.desc())
            .all()
        )

    # Notification
    def save_notification(self, notification, session):
        session.add(notification)
        session.flush()
        return notification

    def get_notifications_by_user(self, user_id, session):
        return (
            session.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.time.desc())
            .limit(100)
            .all()
        )

    def get_notification(self, notification_id, session):
        return session.query(Notification).filter(Notification.id == notification_id).first()

    # SpotRequest
    def save_spot_request(self, spot_request, session):
        session.add(spot_request)
        session.flush()
        return spot_request

    def get_spot_request(self, spot_request_id, session):
        return session.query(Spot_Request).filter(Spot_Request.id == spot_request_id).first()

    def get_incoming_spot_requests(self, user_id, session):
        # user is the spotter being asked
        return session.query(Spot_Request).filter(Spot_Request.spotter_id == user_id).all()

    def get_outgoing_spot_requests(self, user_id, session):
        return session.query(Spot_Request).filter(Spot_Request.requester_id == user_id).all()

    def delete_spot_request(self, spot_request_id, session):
        req = session.query(Spot_Request).filter(Spot_Request.id == spot_request_id).first()
        if req:
            session.delete(req)
            session.flush()
        return req
