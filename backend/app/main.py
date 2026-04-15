from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes.users import UserRouter
from app.db.base import Base
from app.db.postgresql.factory import PostgreSQLFactory

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = PostgreSQLFactory.create_db_connection()
    Base.metadata.create_all(bind=connection.engine)
    yield


app = FastAPI(lifespan=lifespan)
    
user_router = UserRouter()
app.include_router(user_router.router)