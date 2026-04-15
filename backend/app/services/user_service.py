
from app.db.repositories import DBRepository
from app.schemas.user import UserCreate
from app.models.user import User

from pwdlib import PasswordHash

class UserService():
    password_hash = PasswordHash.recommended()

    def __init__(self, repo: DBRepository):
        self.repo = repo

    def get_all_users(self):
        return self.repo.get_all_users()

    def create_user(self, user:UserCreate):
        new_user = User()
        new_user.email = user.email
        new_user.password = self.password_hash.hash(user.password)

        return self.repo.save_user(new_user)

    def get_user(self, user_id:int):
        return self.repo.get_user(user_id)