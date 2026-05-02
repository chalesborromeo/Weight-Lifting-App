from abc import ABC, abstractmethod

class DBRepository(ABC):

    @abstractmethod
    def get_user_by_email(self, email, session):pass

    # User
    @abstractmethod
    def get_all_users(self, session): pass

    @abstractmethod
    def save_user(self, user, session): pass

    @abstractmethod
    def get_user(self, user_id, session): pass

    @abstractmethod
    def get_user_suggestions(self, user_id, session): pass

    # Club
    @abstractmethod
    def get_all_clubs(self, session): pass

    @abstractmethod
    def get_club(self, club_id, session): pass

    @abstractmethod
    def save_club(self, club, session): pass

    @abstractmethod
    def delete_club(self, club_id, session): pass

    @abstractmethod
    def get_club_posts(self, club_id, session): pass

    # Workout
    @abstractmethod
    def get_all_workouts(self, session): pass

    @abstractmethod
    def get_users_workouts(self, user_id, session): pass

    @abstractmethod
    def get_workout(self, workout_id, session): pass

    @abstractmethod
    def save_workout(self, workout, session): pass

    @abstractmethod
    def delete_workout(self, workout_id, session): pass

    # Post
    @abstractmethod
    def save_post(self, post, session): pass

    @abstractmethod
    def get_post(self, post_id, session): pass

    @abstractmethod
    def get_feed_posts(self, user_ids, session): pass

    @abstractmethod
    def delete_post(self, post_id, session): pass

    @abstractmethod
    def get_all_posts(self, session): pass

    # Comment
    @abstractmethod
    def save_comment(self, comment, session): pass

    @abstractmethod
    def get_comments_for_post(self, post_id, session): pass

    # Peer
    @abstractmethod
    def save_peer(self, peer, session): pass

    @abstractmethod
    def get_peer(self, user_id, peer_id, session): pass

    @abstractmethod
    def get_peers_by_user(self, user_id, status, session): pass

    @abstractmethod
    def get_pending_for_user(self, user_id, session): pass

    @abstractmethod
    def delete_peer(self, peer_id, session): pass

    @abstractmethod
    def get_accepted_peer_ids(self, user_id, session): pass

    # Profile
    @abstractmethod
    def get_profile_by_user(self, user_id, session): pass

    @abstractmethod
    def save_profile(self, profile, session): pass

    # User search
    @abstractmethod
    def search_users(self, query, session): pass

    # PR
    @abstractmethod
    def save_pr(self, pr, session): pass

    @abstractmethod
    def get_prs_by_user(self, user_id, session): pass

    @abstractmethod
    def get_pr(self, pr_id, session): pass

    @abstractmethod
    def delete_pr(self, pr_id, session): pass

    @abstractmethod
    def get_top_prs_by_exercise(self, exercise_name, limit, session): pass

    # Gym
    @abstractmethod
    def get_all_gyms(self, session): pass

    @abstractmethod
    def get_gym(self, gym_id, session): pass

    @abstractmethod
    def save_gym(self, gym, session): pass

    # BodyMetric
    @abstractmethod
    def save_body_metric(self, metric, session): pass

    @abstractmethod
    def get_body_metrics_by_user(self, user_id, session): pass

    # FavoriteExercise
    @abstractmethod
    def save_favorite_exercise(self, favorite, session): pass

    @abstractmethod
    def get_favorite_exercises_by_user(self, user_id, session): pass

    @abstractmethod
    def get_favorite_exercise(self, favorite_id, session): pass

    @abstractmethod
    def delete_favorite_exercise(self, favorite_id, session): pass

    # Report
    @abstractmethod
    def save_report(self, report, session): pass

    @abstractmethod
    def get_reports_for_post(self, post_id, session): pass

    @abstractmethod
    def get_unresolved_reports(self, session): pass

    # Notification
    @abstractmethod
    def save_notification(self, notification, session): pass

    @abstractmethod
    def get_notifications_by_user(self, user_id, session): pass

    @abstractmethod
    def get_notification(self, notification_id, session): pass

    # SpotRequest
    @abstractmethod
    def save_spot_request(self, spot_request, session): pass

    @abstractmethod
    def get_spot_request(self, spot_request_id, session): pass

    @abstractmethod
    def get_incoming_spot_requests(self, user_id, session): pass

    @abstractmethod
    def get_outgoing_spot_requests(self, user_id, session): pass

    @abstractmethod
    def delete_spot_request(self, spot_request_id, session): pass
