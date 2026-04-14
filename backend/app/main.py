from fastapi import FastAPI

from backend.app.api.routes.users import UserRouter

app = FastAPI()

user_router = UserRouter()
app.include_router(user_router.router)