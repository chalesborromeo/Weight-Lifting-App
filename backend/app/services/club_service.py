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

    def create_club(self, user_id: int, club: ClubCreate):
        new_club = Club()
        new_club.name = club.name
        new_club.description = club.description
        new_club.owner_id = user_id
        new_club.privacy = club.privacy
        self.repo.save_club(new_club, self.session)
        return new_club

    def join_club(self, user_id: int, club_id: int):
        user = self.repo.get_user(user_id, self.session)
        club = self.repo.get_club(club_id, self.session)
        if not club:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")
        if any(m.id == user_id for m in club.members):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already a member")
        club.members.append(user)
        self.repo.save_club(club, self.session)
        self.session.refresh(club)
        return club

    def leave_club(self, requester_id: int, member_id: int, club_id: int):
        club = self.repo.get_club(club_id, self.session)
        if not club:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")

        # Only the owner can remove someone else; otherwise you can only remove yourself.
        if requester_id != member_id and club.owner_id != requester_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the club owner can remove other members")

        member = self.repo.get_user(member_id, self.session)
        if not member or not any(m.id == member_id for m in club.members):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found in club")

        club.members.remove(member)
        self.repo.save_club(club, self.session)
        self.session.refresh(club)
        return club

    def delete_club(self, user_id: int, club_id: int):
        club = self.repo.get_club(club_id, self.session)
        if not club:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")
        if club.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the club owner can delete this club")
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
