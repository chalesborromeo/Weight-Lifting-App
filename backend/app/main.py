from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.users import UserRouter
from app.api.routes.clubs import ClubRouter
from app.api.routes.workouts import WorkoutRouter
from app.api.routes.auth import AuthRouter
from app.api.routes.posts import PostRouter
from app.api.routes.peers import PeerRouter
from app.api.routes.profiles import ProfileRouter
from app.api.routes.prs import PRRouter
from app.api.routes.gyms import GymRouter
from app.api.routes.body_metrics import BodyMetricRouter
from app.api.routes.favorite_exercises import FavoriteExerciseRouter
from app.api.routes.reports import ReportRouter
from app.api.routes.notifications import NotificationRouter
from app.api.routes.spotters import SpotterRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter().router)
app.include_router(UserRouter().router)
app.include_router(ProfileRouter().router)
app.include_router(ClubRouter().router)
app.include_router(WorkoutRouter().router)
app.include_router(PostRouter().router)
app.include_router(PeerRouter().router)
app.include_router(PRRouter().router)
app.include_router(GymRouter().router)
app.include_router(BodyMetricRouter().router)
app.include_router(FavoriteExerciseRouter().router)
app.include_router(ReportRouter().router)
app.include_router(NotificationRouter().router)
app.include_router(SpotterRouter().router)

UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
