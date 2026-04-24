from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes.auth import AuthRouter
from app.api.routes.users import UserRouter
from app.api.routes.clubs import ClubRouter
from app.api.routes.workouts import WorkoutRouter
from app.api.routes.posts import PostRouter
from app.api.routes.spotters import SpottersRouter
from app.api.routes.peers import PeersRouter
from app.api.routes.notifications import NotificationsRouter
from app.db.base import Base
from app.db.postgresql.factory import PostgreSQLFactory
from app import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = PostgreSQLFactory.create_db_connection()
    Base.metadata.create_all(bind=connection.engine)
    yield


app = FastAPI(lifespan=lifespan)
    
auth_router = AuthRouter()
user_router = UserRouter()
club_router = ClubRouter()
workout_router = WorkoutRouter()
post_router = PostRouter()
spotters_router = SpottersRouter()
peers_router = PeersRouter()
notifications_router = NotificationsRouter()

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(club_router.router)
app.include_router(workout_router.router)
app.include_router(post_router.router)
app.include_router(spotters_router.router)
app.include_router(peers_router.router)
app.include_router(notifications_router.router)