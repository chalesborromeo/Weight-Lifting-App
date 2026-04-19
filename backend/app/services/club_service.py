
from app.models.club import Club
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
        
