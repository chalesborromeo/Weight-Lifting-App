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

    # Club
    @abstractmethod
    def get_all_clubs(self, session): pass

    @abstractmethod
    def get_club(self, club_id, session): pass

    @abstractmethod
    def save_club(self, club, session): pass

    @abstractmethod
    def delete_club(self, club_id, session): pass

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
