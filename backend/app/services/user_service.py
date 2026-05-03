from datetime import date, timedelta
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

    def create_user(self, user: UserCreate):
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

    def get_user(self, user_id: int):
        return self.repo.get_user(user_id, self.session)

    def search_users(self, query: str):
        return self.repo.search_users(query, self.session)

    def get_streak(self, user_id: int) -> int:
        workouts = self.repo.get_users_workouts(user_id, self.session)
        if not workouts:
            return 0

        workout_dates = sorted(
            {w.created_at.date() for w in workouts if w.created_at},
            reverse=True,
        )
        if not workout_dates:
            return 0

        today = date.today()
        if workout_dates[0] < today - timedelta(days=1):
            return 0

        streak = 0
        expected = workout_dates[0]
        for d in workout_dates:
            if d == expected:
                streak += 1
                expected -= timedelta(days=1)
            else:
                break

        return streak

    def get_suggestions(self, user_id: int):
        return self.repo.get_user_suggestions(user_id, self.session)

    def export_data(self, user_id: int) -> dict:
        user = self.repo.get_user(user_id, self.session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        profile = self.repo.get_profile_by_user(user_id, self.session)
        workouts = self.repo.get_users_workouts(user_id, self.session)
        prs = self.repo.get_prs_by_user(user_id, self.session)
        metrics = self.repo.get_body_metrics_by_user(user_id, self.session)
        favorites = self.repo.get_favorite_exercises_by_user(user_id, self.session)
        checkins = self.repo.get_checkins_by_user(user_id, self.session)

        def fmt_workout(w):
            return {
                "id": w.id,
                "name": w.name,
                "type": w.type,
                "duration": w.duration,
                "is_public": w.is_public,
                "created_at": w.created_at.isoformat() if w.created_at else None,
                "exercises": [
                    {
                        "name": e.name,
                        "sets": [{"weight": s.weight, "reps": s.reps} for s in e.sets],
                    }
                    for e in w.exercises
                ],
            }

        return {
            "user": {"id": user.id, "email": user.email},
            "profile": {
                "first_name": profile.first_name if profile else None,
                "last_name": profile.last_name if profile else None,
                "bio": profile.bio if profile else None,
            } if profile else None,
            "workouts": [fmt_workout(w) for w in workouts],
            "personal_records": [
                {"exercise": p.exercise_name, "weight": p.weight, "reps": p.reps,
                 "date": p.date.isoformat() if p.date else None}
                for p in prs
            ],
            "body_metrics": [
                {"weight": m.weight, "recorded_at": m.recorded_at.isoformat() if m.recorded_at else None}
                for m in metrics
            ],
            "favorite_exercises": [f.name for f in favorites],
            "gym_checkins": [
                {"gym_name": c.gym_name, "gym_address": c.gym_address,
                 "checked_in_at": c.checked_in_at.isoformat() if c.checked_in_at else None}
                for c in checkins
            ],
        }
