from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.schemas.suggestion import ExerciseSuggestion, WorkoutSuggestion


class SuggestionService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def get_workout_suggestion(self, user_id: int) -> WorkoutSuggestion:
        # Get user's favorite exercises
        favorites = self.repo.get_favorite_exercises_by_user(user_id, self.session)

        if not favorites:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No favorite exercises found. Please add favorite exercises first."
            )

        exercise_suggestions = []

        # Generate suggestions for each favorite (limit to 4-6 exercises)
        for favorite in favorites[:6]:
            suggestion = self._generate_exercise_suggestion(user_id, favorite.name)
            if suggestion:
                exercise_suggestions.append(suggestion)

        if not exercise_suggestions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unable to generate suggestions. Please complete some workouts first."
            )

        # Estimate duration: ~10-15 min per exercise
        estimated_duration = len(exercise_suggestions) * 12.5

        day = datetime.now().strftime("%A")
        return WorkoutSuggestion(
            workout_name=f"{day} Workout",
            workout_type="Personalized",
            estimated_duration=estimated_duration,
            exercises=exercise_suggestions,
            total_exercises=len(exercise_suggestions)
        )

    def _generate_exercise_suggestion(self, user_id: int, exercise_name: str) -> ExerciseSuggestion:
        # Get recent performance for this exercise (last 3 workouts)
        recent_workouts = self.repo.get_recent_exercise_performance(
            user_id, exercise_name, 3, self.session
        )

        if not recent_workouts:
            # No history - suggest conservative starting weights
            return ExerciseSuggestion(
                exercise_name=exercise_name,
                suggested_sets=3,
                suggested_reps=10,
                suggested_weight=None,
                previous_best_weight=None,
                previous_best_reps=None,
                rationale="No workout history. Start with a comfortable weight for 10 reps."
            )

        # Extract all sets for this exercise from recent workouts
        all_sets = []
        for workout in recent_workouts:
            for exercise in workout.exercises:
                if exercise.name == exercise_name:
                    all_sets.extend(exercise.sets)

        if not all_sets:
            # Edge case: workouts exist but no sets recorded
            return ExerciseSuggestion(
                exercise_name=exercise_name,
                suggested_sets=3,
                suggested_reps=10,
                suggested_weight=None,
                previous_best_weight=None,
                previous_best_reps=None,
                rationale="No set data found. Start with a comfortable weight."
            )

        # Calculate statistics from recent sets
        avg_weight = sum(s.weight for s in all_sets if s.weight) / len([s for s in all_sets if s.weight])
        max_weight = max(s.weight for s in all_sets if s.weight)
        avg_reps = sum(s.reps for s in all_sets) / len(all_sets)
        max_reps = max(s.reps for s in all_sets)

        # Check if there's been a long gap since last workout (deload if >14 days)
        last_workout_date = recent_workouts[0].created_at
        days_since_last = (datetime.now() - last_workout_date).days

        if days_since_last > 14:
            # Deload - reduce weight by 10%
            suggested_weight = round(avg_weight * 0.9, 1)
            suggested_reps = int(avg_reps)
            rationale = f"It's been {days_since_last} days since your last workout. Starting with a deload (10% lighter)."
        else:
            # Apply progressive overload
            suggested_weight, suggested_reps, rationale = self._calculate_progressive_overload(
                avg_weight, avg_reps, max_reps
            )

        return ExerciseSuggestion(
            exercise_name=exercise_name,
            suggested_sets=3,
            suggested_reps=suggested_reps,
            suggested_weight=suggested_weight,
            previous_best_weight=max_weight,
            previous_best_reps=max_reps,
            rationale=rationale
        )

    def _calculate_progressive_overload(self, avg_weight: float, avg_reps: float, max_reps: int) -> tuple:
        """
        Calculate progressive overload based on recent performance.
        Returns: (suggested_weight, suggested_reps, rationale)
        """
        # If average reps are high (12+), increase weight and drop reps
        if avg_reps >= 12:
            suggested_weight = round(avg_weight + 5, 1)  # +5 lbs
            suggested_reps = 8
            rationale = f"Based on your recent performance, increase weight by 5 lbs and aim for 8 reps."

        # If reps are moderate (8-11), try to increase reps first
        elif 8 <= avg_reps < 12:
            suggested_weight = round(avg_weight, 1)  # Keep weight same
            suggested_reps = int(avg_reps) + 1
            rationale = f"Keep the same weight and try for {suggested_reps} reps (progressive overload)."

        # If reps are low (<8), increase weight slightly
        else:
            suggested_weight = round(avg_weight + 2.5, 1)  # +2.5 lbs
            suggested_reps = max(8, int(avg_reps))
            rationale = f"Increase weight by 2.5 lbs and aim for {suggested_reps} reps."

        return suggested_weight, suggested_reps, rationale
