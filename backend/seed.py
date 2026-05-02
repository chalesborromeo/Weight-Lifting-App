"""
Run from the backend/ directory with the venv active:
    python seed.py
Idempotent — skips bot accounts that already exist.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timezone, timedelta
from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.respository import PostgreSQLRepository
from app.models.user import User
from app.models.profile import Profile
from app.models.post import Post
from app.core.security import hash_password

BOTS = [
    {
        "email": "ironmike@spotter.app",
        "password": "SpotterBot!1",
        "first_name": "Mike",
        "last_name": "Iron",
        "bio": "Powerlifter. 4x/week. Squat is life.",
        "posts": [
            "Just hit 405 on squat for the first time. Years of work paying off.",
            "Leg day reminder: if you can walk normally the next day, you didn't go hard enough.",
            "New PR on deadlift — 455 lbs. The bar had to move eventually.",
        ],
    },
    {
        "email": "gainzgabby@spotter.app",
        "password": "SpotterBot!2",
        "first_name": "Gabby",
        "last_name": "Gainz",
        "bio": "Hypertrophy focused. Meal prep queen. Here to grow.",
        "posts": [
            "12 weeks of consistent training and the results are finally showing. Trust the process.",
            "Prepped my meals for the whole week. Chicken, rice, and broccoli never looked so good.",
            "Push day done. Chest is wrecked. Time to eat.",
        ],
    },
    {
        "email": "cardioking@spotter.app",
        "password": "SpotterBot!3",
        "first_name": "Carlos",
        "last_name": "Reyes",
        "bio": "Running + lifting combo. Half marathon in March.",
        "posts": [
            "5 mile run before the gym. Some call it crazy. I call it Wednesday.",
            "Just finished a 90 min full body session. Legs, back, and a 2 mile cooldown run.",
            "Rest day? More like active recovery day. Light jog, stretch, foam roll. Never stop moving.",
        ],
    },
    {
        "email": "benchpressqueen@spotter.app",
        "password": "SpotterBot!4",
        "first_name": "Aisha",
        "last_name": "Okonkwo",
        "bio": "225 bench is the goal. Currently at 185. Let's get it.",
        "posts": [
            "185 lb bench press today. PR. The grind is real.",
            "Upper body day: bench, OHP, rows, curls. Shoulders are toast.",
            "Someone asked if I needed a spotter. I said yes. That's the whole point of this app.",
        ],
    },
]


def seed():
    conn = PostgreSQLConnection.get_instance()
    repo = PostgreSQLRepository()

    with conn.get_session() as session:
        for i, bot in enumerate(BOTS):
            existing = repo.get_user_by_email(bot["email"], session)
            if existing:
                print(f"  skip {bot['email']} (already exists)")
                continue

            user = User()
            user.email = bot["email"]
            user.password = hash_password(bot["password"])
            repo.save_user(user, session)

            profile = Profile()
            profile.user_id = user.id
            profile.first_name = bot["first_name"]
            profile.last_name = bot["last_name"]
            profile.bio = bot["bio"]
            repo.save_profile(profile, session)

            for j, text in enumerate(bot["posts"]):
                post = Post()
                post.user_id = user.id
                post.text = text
                # stagger dates so they don't all appear at the exact same time
                post.date = datetime.now(timezone.utc) - timedelta(hours=(i * 10 + j * 3))
                repo.save_post(post, session)

            print(f"  created {bot['email']} with {len(bot['posts'])} posts")

    print("Seed complete.")


if __name__ == "__main__":
    seed()
