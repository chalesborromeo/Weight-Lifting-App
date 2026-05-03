from typing import List

from fastapi import APIRouter, Depends

from app.services.workout_service import WorkoutService
from app.db.postgresql.factory import PostgreSQLFactory
from app.schemas.workout import WorkoutCreate, WorkoutResponse
from app.core.security import get_current_user_id
from app.api.deps import get_db

def get_workout_service(session=Depends(get_db)) -> WorkoutService:
    repo = PostgreSQLFactory.create_db_repository()
    return WorkoutService(repo, session)

class WorkoutRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/workouts", tags=["workouts"])
        self.router.add_api_route("/", self.get_all, methods=["GET"], response_model=List[WorkoutResponse])
        self.router.add_api_route("/", self.create, methods=["POST"], response_model=WorkoutResponse)
        self.router.add_api_route("/user/{user_id}", self.get_users_all, methods=["GET"], response_model=List[WorkoutResponse])
        self.router.add_api_route("/{workout_id}", self.get_one, methods=["GET"], response_model=WorkoutResponse)
        self.router.add_api_route("/{workout_id}", self.delete, methods=["DELETE"], response_model=WorkoutResponse)

        
    async def get_all(self, service: WorkoutService = Depends(get_workout_service)):
        return service.get_all_workouts()
    
    async def create(self, workout:WorkoutCreate, service: WorkoutService = Depends(get_workout_service)):
        return service.create_workout(workout)

    async def get_users_all(
        self,
        user_id: int,
        requester_id: int = Depends(get_current_user_id),
        service: WorkoutService = Depends(get_workout_service),
    ):
        workouts = service.get_users_workouts(user_id)
        if requester_id != user_id:
            workouts = [w for w in workouts if w.is_public]
        return workouts
    
    async def get_one(self, workout_id:int, service: WorkoutService = Depends(get_workout_service)):
        return service.get_workout(workout_id)
    
    async def delete(self, workout_id:int, service: WorkoutService = Depends(get_workout_service)):
        return service.delete_workout(workout_id)

