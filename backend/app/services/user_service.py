from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.schemas.user import UserCreate
from app.models.user import User

from pwdlib import PasswordHash

class UserService():
    password_hash = PasswordHash.recommended()

    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def get_all_users(self):
        return self.repo.get_all_users(self.session)

    def create_user(self, user:UserCreate):
        if self.repo.get_user_by_email(user.email, self.session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        new_user = User()
        new_user.email = user.email
        new_user.password = self.password_hash.hash(user.password)

        self.repo.save_user(new_user, self.session)
        return new_user

    def get_user(self, user_id:int):
        return self.repo.get_user(user_id, self.session)

    def search_users(self, query: str):
        return self.repo.search_users(query, self.session)