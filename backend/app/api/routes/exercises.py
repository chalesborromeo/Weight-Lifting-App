from typing import List

from fastapi import APIRouter

# High-level activity/sport types a user picks for a workout session.
# Ordered from most common (gym-centric) to niche.
WORKOUT_TYPES: List[str] = [
    "Strength",
    "Cardio",
    "HIIT",
    "Running",
    "Cycling",
    "Swimming",
    "Rowing",
    "Yoga",
    "CrossFit",
    "Stretching",
    "Other",
]

# Static catalog of common exercises grouped by primary muscle.
# Keep names canonical so PRs/leaderboards group correctly.
EXERCISE_CATALOG: List[dict] = [
    # Chest
    {"name": "Bench Press", "group": "Chest"},
    {"name": "Incline Bench Press", "group": "Chest"},
    {"name": "Dumbbell Bench Press", "group": "Chest"},
    {"name": "Push-Up", "group": "Chest"},
    {"name": "Cable Fly", "group": "Chest"},
    # Back
    {"name": "Deadlift", "group": "Back"},
    {"name": "Pull-Up", "group": "Back"},
    {"name": "Barbell Row", "group": "Back"},
    {"name": "Lat Pulldown", "group": "Back"},
    {"name": "Seated Cable Row", "group": "Back"},
    # Legs
    {"name": "Back Squat", "group": "Legs"},
    {"name": "Front Squat", "group": "Legs"},
    {"name": "Romanian Deadlift", "group": "Legs"},
    {"name": "Leg Press", "group": "Legs"},
    {"name": "Lunge", "group": "Legs"},
    {"name": "Leg Curl", "group": "Legs"},
    {"name": "Leg Extension", "group": "Legs"},
    {"name": "Calf Raise", "group": "Legs"},
    # Shoulders
    {"name": "Overhead Press", "group": "Shoulders"},
    {"name": "Dumbbell Shoulder Press", "group": "Shoulders"},
    {"name": "Lateral Raise", "group": "Shoulders"},
    {"name": "Face Pull", "group": "Shoulders"},
    # Arms
    {"name": "Barbell Curl", "group": "Arms"},
    {"name": "Dumbbell Curl", "group": "Arms"},
    {"name": "Hammer Curl", "group": "Arms"},
    {"name": "Tricep Pushdown", "group": "Arms"},
    {"name": "Skullcrusher", "group": "Arms"},
    {"name": "Dip", "group": "Arms"},
    # Core
    {"name": "Plank", "group": "Core"},
    {"name": "Hanging Leg Raise", "group": "Core"},
    {"name": "Cable Crunch", "group": "Core"},
    # Cardio / conditioning
    {"name": "Running", "group": "Cardio"},
    {"name": "Rowing", "group": "Cardio"},
    {"name": "Cycling", "group": "Cardio"},
]


class ExerciseRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/exercises", tags=["exercises"])
        self.router.add_api_route("/catalog", self.catalog, methods=["GET"])
        self.router.add_api_route("/workout-types", self.workout_types, methods=["GET"])

    async def catalog(self):
        """Return the canonical exercise catalog used for PR/workout autocomplete."""
        return EXERCISE_CATALOG

    async def workout_types(self):
        """Return the canonical list of workout session types (Strava-style)."""
        return WORKOUT_TYPES
