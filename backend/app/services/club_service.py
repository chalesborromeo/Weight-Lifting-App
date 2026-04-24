
from fastapi import HTTPException, status

from app.models.club import Club
from app.models.post import Post
from app.schemas.club import ClubCreate
from app.db.repositories import DBRepository


class ClubService():
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def get_all_clubs(self):
        return self.repo.get_all_clubs(self.session)
    
    def get_club(self, club_id):
        return self.repo.get_club(club_id, self.session)
    
    def create_club(self, club:ClubCreate):
        new_club = Club()
        new_club.name = club.name
        new_club.description = club.description
        new_club.owner_id = club.owner_id
        new_club.privacy = club.privacy

        self.repo.save_club(new_club, self.session)
        self.session.refresh(new_club)
        return new_club
    
    def join_club(self, user_id, club_id):
        user = self.repo.get_user(user_id, self.session)
        club = self.repo.get_club(club_id, self.session)

        club.members.append(user)
        self.repo.save_club(club, self.session)
        self.session.refresh(club)
        return club
    
    def leave_club(self, user_id, club_id):
        user = self.repo.get_user(user_id, self.session)
        club = self.repo.get_club(club_id, self.session)

        club.members.remove(user)
        self.repo.save_club(club, self.session)
        self.session.refresh(club)
        return club
    
    def delete_club(self, club_id):
        club = self.repo.get_club(club_id, self.session)
        if club:
            self.repo.delete_club(club_id, self.session)
        return club

    def get_club_feed(self, club_id):
        return self.repo.get_club_posts(club_id, self.session)

    def create_club_post(self, club_id, user_id, text):
        club = self.repo.get_club(club_id, self.session)
        if not club:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")
        member_ids = [m.id for m in club.members]
        if user_id not in member_ids and club.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Must be a member to post")
        post = Post()
        post.user_id = user_id
        post.club_id = club_id
        post.text = text
        self.repo.save_post(post, self.session)
        self.session.refresh(post)
        return post
