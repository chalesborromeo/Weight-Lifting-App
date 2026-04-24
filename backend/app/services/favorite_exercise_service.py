from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.db.repositories import DBRepository
from app.models.favorite_exercise import FavoriteExercise
from app.schemas.favorite_exercise import FavoriteExerciseCreate


class FavoriteExerciseService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def add_favorite(self, user_id: int, data: FavoriteExerciseCreate):
        favorite = FavoriteExercise(user_id=user_id, name=data.name)
        try:
            self.repo.save_favorite_exercise(favorite, self.session)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exercise already favorited")
        self.session.refresh(favorite)
        return favorite

    def list_favorites(self, user_id: int):
        return self.repo.get_favorite_exercises_by_user(user_id, self.session)

    def remove_favorite(self, user_id: int, favorite_id: int):
        favorite = self.repo.get_favorite_exercise(favorite_id, self.session)
        if not favorite:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
        if favorite.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot remove another user's favorite")
        self.repo.delete_favorite_exercise(favorite_id, self.session)
        return {"message": "Favorite removed"}
