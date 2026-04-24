import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.db.repositories import DBRepository
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate

ALLOWED_PICTURE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_PICTURE_BYTES = 5 * 1024 * 1024  # 5 MB
UPLOADS_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"


class ProfileService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def get_my_profile(self, user_id: int):
        profile = self.repo.get_profile_by_user(user_id, self.session)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        return profile

    def create_profile(self, user_id: int, data: ProfileCreate):
        existing = self.repo.get_profile_by_user(user_id, self.session)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile already exists")

        profile = Profile(user_id=user_id, **data.model_dump(exclude_unset=True))
        self.repo.save_profile(profile, self.session)
        self.session.refresh(profile)
        return profile

    def update_profile(self, user_id: int, data: ProfileUpdate):
        profile = self.repo.get_profile_by_user(user_id, self.session)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)

        self.session.flush()
        self.session.refresh(profile)
        return profile

    async def upload_picture(self, user_id: int, file: UploadFile):
        if file.content_type not in ALLOWED_PICTURE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image type: {file.content_type}",
            )

        contents = await file.read()
        if len(contents) > MAX_PICTURE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large (max 5 MB)",
            )

        profile = self.repo.get_profile_by_user(user_id, self.session)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        # Pick extension from content type, not the user-supplied filename.
        extension = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
            "image/gif": ".gif",
        }[file.content_type]

        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"{uuid.uuid4().hex}{extension}"
        (UPLOADS_DIR / filename).write_bytes(contents)

        profile.profile_picture_url = f"/uploads/{filename}"
        self.session.flush()
        self.session.refresh(profile)
        return profile

    def set_gym(self, user_id: int, gym_id: int):
        gym = self.repo.get_gym(gym_id, self.session)
        if not gym:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found")

        profile = self.repo.get_profile_by_user(user_id, self.session)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        profile.gym_id = gym_id
        self.session.flush()
        self.session.refresh(profile)
        return profile
