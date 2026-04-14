
from backend.app.db.repositories import DBRepository
from backend.app.schemas.user import UserCreate


class UserService():
    def __init___(self, repo: DBRepository):
        self.repo = repo

    def get_all_users(self):
        return self.repo.get_all_users()

    def create_user(self, user:UserCreate):
        new_user = User() # import from /models
        new_user.email = user.email
        new_user.password = user.password

        return self.repo.save_user(new_user)

    def get_user(self, user_id:int):
        return self.repo.get_user(user_id)