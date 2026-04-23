
from app.db.repositories import DBRepository
from app.schemas.workout import WorkoutCreate
from app.models.workout import Workout
from app.models.exercise import Exercise
from app.models.sets import Sets
from app.models.post import Post

class WorkoutService():
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def get_all_workouts(self):
        return self.repo.get_all_workouts(self.session)
    
    def get_users_workouts(self, user_id):
        return self.repo.get_users_workouts(user_id, self.session)
    
    def get_workout(self, workout_id):
        return self.repo.get_workout(workout_id, self.session)
    
    def create_workout(self, workout:WorkoutCreate):
        new_workout = Workout()
        new_workout.name = workout.name
        new_workout.type = workout.type
        new_workout.duration = workout.duration
        new_workout.user_id = workout.user_id

        new_exercises = []
        for exercise in workout.exercises:
            new_exercise = Exercise()
            new_exercise.name = exercise.name

            new_sets = []
            for s in exercise.sets:
                new_set = Sets()
                new_set.weight = s.weight
                new_set.reps= s.reps
            
                new_sets.append(new_set)

            new_exercise.sets = new_sets
            new_exercises.append(new_exercise)
    
        new_workout.exercises = new_exercises

        self.repo.save_workout(new_workout, self.session)
        self.session.refresh(new_workout)

        # Auto-create a post for this workout
        post = Post()
        post.user_id = new_workout.user_id
        post.workout_id = new_workout.id
        post.text = f"Just completed {new_workout.name}"
        self.repo.save_post(post, self.session)

        return new_workout

    def delete_workout(self, workout_id):
        workout = self.repo.get_workout(workout_id, self.session)
        if workout:
            self.repo.delete_workout(workout_id, self.session)

        return workout