from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.models.pr import PR
from app.models.post import Post
from app.schemas.pr import PRCreate


class PRService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def create_pr(self, user_id: int, data: PRCreate):
        pr = PR(user_id=user_id, **data.model_dump())
        self.repo.save_pr(pr, self.session)
        self.session.refresh(pr)

        milestone = Post()
        milestone.user_id = user_id
        milestone.text = f"🏆 NEW PR — {data.exercise_name}: {data.weight} lbs × {data.reps} reps"
        self.repo.save_post(milestone, self.session)

        return pr

    def list_prs(self, user_id: int):
        return self.repo.get_prs_by_user(user_id, self.session)

    def delete_pr(self, user_id: int, pr_id: int):
        pr = self.repo.get_pr(pr_id, self.session)
        if not pr:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PR not found")
        if pr.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete another user's PR")
        self.repo.delete_pr(pr_id, self.session)
        return {"message": "PR deleted"}

    def leaderboard(self, exercise_name: str, limit: int = 10):
        return self.repo.get_top_prs_by_exercise(exercise_name, limit, self.session)
