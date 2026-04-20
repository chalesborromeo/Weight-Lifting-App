from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes.users import UserRouter
from app.api.routes.clubs import ClubRouter
from app.api.routes.workouts import WorkoutRouter
from app.db.base import Base
from app.db.postgresql.factory import PostgreSQLFactory
from app.models import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = PostgreSQLFactory.create_db_connection()
    Base.metadata.create_all(bind=connection.engine)
    yield


app = FastAPI(lifespan=lifespan)
    
user_router = UserRouter()
club_router= ClubRouter()
workout_router = WorkoutRouter()
app.include_router(user_router.router)
app.include_router(club_router.router)
app.include_route(workout_router.router)