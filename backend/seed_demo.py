"""
Demo seed script — populates the database with realistic data for a presentation.
Run from the backend directory with the venv active:
    python seed_demo.py

Demo login: demo@spotter.app / demo1234
"""

import app.models.user, app.models.workout, app.models.exercise, app.models.sets
import app.models.post, app.models.comment, app.models.peer, app.models.profile
import app.models.pr, app.models.gym, app.models.gym_checkin, app.models.body_metric
import app.models.favorite_exercise, app.models.notification, app.models.report
import app.models.spot_Request, app.models.club

from app.db.postgresql.connection import PostgreSQLConnection
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.workout import Workout
from app.models.exercise import Exercise
from app.models.sets import Sets
from app.models.pr import PR
from app.models.profile import Profile
from app.models.peer import Peer
from app.models.favorite_exercise import FavoriteExercise
from app.models.body_metric import BodyMetric
from app.models.gym_checkin import GymCheckIn
from pwdlib import PasswordHash
from datetime import datetime, timedelta, date
import random

random.seed(42)
pw = PasswordHash.recommended()
conn = PostgreSQLConnection.get_instance()

DEMO_EMAIL = "demo@spotter.app"
DEMO_PASSWORD = "demo1234"

# ── Personas ──────────────────────────────────────────────────────────────────
PERSONAS = [
    {
        "email": DEMO_EMAIL,
        "password": DEMO_PASSWORD,
        "first_name": "Alex",
        "last_name": "Rivera",
        "bio": "Powerlifter & Spotter user. Chasing strength every day 🏋️",
        "athlete_type": "powerlifter",
        "is_demo": True,
    },
    {
        "email": "marcus.t@spotter.app",
        "password": "password123",
        "first_name": "Marcus",
        "last_name": "Thompson",
        "bio": "3x state powerlifting champion. Deadlift: 575lbs and climbing 🔥",
        "athlete_type": "powerlifter",
    },
    {
        "email": "sofia.r@spotter.app",
        "password": "password123",
        "first_name": "Sofia",
        "last_name": "Reyes",
        "bio": "HIIT coach & fitness influencer. Come get humbled in my 6am class 💪",
        "athlete_type": "hiit",
    },
    {
        "email": "jalen.w@spotter.app",
        "password": "password123",
        "first_name": "Jalen",
        "last_name": "Williams",
        "bio": "College football | WR | Off-season never stops 🏈",
        "athlete_type": "athlete",
    },
    {
        "email": "priya.m@spotter.app",
        "password": "password123",
        "first_name": "Priya",
        "last_name": "Mehta",
        "bio": "Marathon runner turned lifter. Faster miles, stronger legs 🏃‍♀️",
        "athlete_type": "runner",
    },
    {
        "email": "derek.c@spotter.app",
        "password": "password123",
        "first_name": "Derek",
        "last_name": "Chen",
        "bio": "Bodybuilder. 12 weeks out from my first show. Dialed in 🏆",
        "athlete_type": "bodybuilder",
    },
]

WORKOUTS = {
    "powerlifter": [
        ("Heavy Squat Day", "Strength", 90, [
            ("Back Squat", [(315, 5), (335, 3), (355, 1)]),
            ("Romanian Deadlift", [(225, 8), (225, 8)]),
            ("Leg Press", [(450, 10), (450, 10)]),
        ]),
        ("Deadlift Session", "Strength", 75, [
            ("Deadlift", [(405, 3), (455, 1), (495, 1)]),
            ("Barbell Row", [(185, 8), (185, 8), (185, 8)]),
            ("Pull-Ups", [(0, 10), (0, 8)]),
        ]),
        ("Bench & Accessories", "Strength", 60, [
            ("Bench Press", [(225, 5), (245, 3), (265, 1)]),
            ("Incline Dumbbell Press", [(85, 8), (85, 8)]),
            ("Tricep Pushdown", [(70, 12), (70, 12)]),
        ]),
    ],
    "hiit": [
        ("HIIT Circuit A", "HIIT", 40, [
            ("Burpees", [(0, 20), (0, 20), (0, 20)]),
            ("Box Jumps", [(0, 15), (0, 15)]),
            ("Kettlebell Swings", [(35, 20), (35, 20)]),
        ]),
        ("Full Body Burn", "HIIT", 45, [
            ("Jump Squats", [(0, 15), (0, 15), (0, 15)]),
            ("Push-Ups", [(0, 25), (0, 25)]),
            ("Mountain Climbers", [(0, 30), (0, 30)]),
        ]),
    ],
    "athlete": [
        ("Speed & Power", "Strength", 70, [
            ("Power Clean", [(135, 5), (155, 4), (175, 3)]),
            ("Box Squat", [(275, 5), (275, 5)]),
            ("Broad Jump", [(0, 5), (0, 5)]),
        ]),
        ("Upper Explosion", "Strength", 55, [
            ("Bench Press", [(185, 8), (205, 6), (225, 4)]),
            ("Weighted Pull-Ups", [(45, 6), (45, 6)]),
            ("Medicine Ball Slam", [(20, 12), (20, 12)]),
        ]),
    ],
    "runner": [
        ("Leg Strength", "Strength", 50, [
            ("Goblet Squat", [(55, 12), (55, 12), (55, 12)]),
            ("Single Leg Press", [(135, 10), (135, 10)]),
            ("Calf Raises", [(0, 20), (0, 20), (0, 20)]),
        ]),
        ("Core & Stability", "Strength", 35, [
            ("Plank", [(0, 60), (0, 60)]),
            ("Dead Bug", [(0, 10), (0, 10)]),
            ("Cable Woodchop", [(40, 12), (40, 12)]),
        ]),
    ],
    "bodybuilder": [
        ("Chest & Triceps", "Bodybuilding", 75, [
            ("Bench Press", [(185, 10), (185, 10), (185, 10)]),
            ("Cable Fly", [(50, 15), (50, 15), (50, 15)]),
            ("Skull Crushers", [(75, 12), (75, 12), (75, 12)]),
        ]),
        ("Back & Biceps", "Bodybuilding", 70, [
            ("Lat Pulldown", [(140, 12), (140, 12), (140, 12)]),
            ("Seated Cable Row", [(120, 12), (120, 12)]),
            ("Barbell Curl", [(65, 12), (65, 12), (65, 12)]),
        ]),
        ("Legs", "Bodybuilding", 80, [
            ("Leg Press", [(360, 15), (360, 15), (360, 15)]),
            ("Leg Extension", [(110, 15), (110, 15)]),
            ("Standing Calf Raise", [(0, 20), (0, 20), (0, 20)]),
        ]),
    ],
}

POST_TEXTS = {
    "powerlifter": [
        "495lb deadlift moved easy today. The 500 is happening this month. 🔥",
        "355lb squat — clean single, no grind. Form is locked in.",
        "Rest day. Just means I'm planning tomorrow's pull session in my head 😂",
        "Competed last weekend. 3/3 on squats for the first time ever.",
        "Bench went up 10lbs this cycle. Slow progress beats no progress.",
    ],
    "hiit": [
        "45 min of pure chaos and I feel incredible 🔥 New circuit is BRUTAL.",
        "Teaching my 6am class tomorrow. Come get humbled if you're local 😈",
        "Foam rolling and mobility today. Recovery is part of the program.",
        "HIIT clears your head like nothing else. Stress? Gone. Problems? Who cares.",
        "Modified today's circuit for a client with a knee injury. Coaches adapt.",
    ],
    "athlete": [
        "Power clean hit 185 for 3 CLEAN reps. 10lb PR and it moved fast 🏈💥",
        "Speed work + heavy lifting = the formula nobody talks about enough.",
        "Off-season is where championships are built. Nobody sees this. That's fine.",
        "First in the weight room at 6am. Last to leave. That's just how it goes.",
        "175lb power clean floating. Explosiveness is a skill I'm mastering.",
    ],
    "runner": [
        "8 mile run then a leg workout. Yes, in that order. I'd do it again 😅",
        "Adding lifting changed my running completely. Less fatigue, faster times.",
        "Goal: sub-7 mile AND 135lb goblet squat x15. Both happening next month.",
        "My calves used to cramp at mile 18. Calf raises changed my life.",
        "Stability work is boring and my knees have never felt better.",
    ],
    "bodybuilder": [
        "12 weeks out. Diet locked, training dialed in. Ready for the stage 🏆",
        "Back and bi's today. Left the gym barely fitting through the door 😂",
        "Pump was absolutely insane today. Days like this are why I do this.",
        "Starting carb cycling this week. The fun begins... or ends. We'll see.",
        "Posing practice at 10pm after a full day. Prep never stops.",
    ],
}

COMMENTS = [
    "Let's go!! 🔥",
    "Absolute beast mode",
    "That's insane progress!",
    "Inspiring as always 💪",
    "You make this look easy",
    "Goals right here 🙌",
    "This is the way",
    "Keep grinding!",
    "That PR is wild bro",
    "This is motivating me to go hit the gym rn",
    "Form looked perfect",
    "You're not human lol",
    "Okay but how 😭",
    "Adding this to my program fr",
    "We don't deserve you 🙏",
]

FAVORITES = {
    "powerlifter": ["Deadlift", "Back Squat", "Bench Press"],
    "hiit": ["Burpees", "Box Jumps", "Kettlebell Swings"],
    "athlete": ["Power Clean", "Box Squat", "Bench Press"],
    "runner": ["Goblet Squat", "Calf Raises", "Plank"],
    "bodybuilder": ["Bench Press", "Lat Pulldown", "Leg Press"],
}

PRS = {
    "powerlifter": [("Deadlift", 495, 1), ("Back Squat", 365, 1), ("Bench Press", 275, 1)],
    "hiit": [("Burpees", 0, 50), ("Box Jumps", 0, 20)],
    "athlete": [("Power Clean", 185, 3), ("Bench Press", 245, 5)],
    "runner": [("Goblet Squat", 65, 15), ("Calf Raises", 0, 25)],
    "bodybuilder": [("Bench Press", 225, 10), ("Leg Press", 450, 15)],
}

GYMS = [
    ("Planet Fitness", "123 Main St, Normal, IL"),
    ("Gold's Gym", "456 College Ave, Bloomington, IL"),
    ("ISU Rec Center", "100 N University St, Normal, IL"),
]


def ago(days=0, hours=0):
    return datetime.now() - timedelta(days=days, hours=hours)


with conn.get_session() as session:
    print("🧹 Clearing old demo data...")
    seed_emails = [p["email"] for p in PERSONAS]
    old_users = session.query(User).filter(User.email.in_(seed_emails)).all()
    for u in old_users:
        session.delete(u)
    session.flush()

    print("👤 Creating personas...")
    created = []
    for persona in PERSONAS:
        u = User()
        u.email = persona["email"]
        u.password = pw.hash(persona["password"])
        session.add(u)
        session.flush()

        prof = Profile()
        prof.user_id = u.id
        prof.first_name = persona["first_name"]
        prof.last_name = persona["last_name"]
        prof.bio = persona["bio"]
        session.add(prof)

        created.append((u, persona))
        tag = " ← DEMO LOGIN" if persona.get("is_demo") else ""
        print(f"   {persona['first_name']} {persona['last_name']} (id={u.id}){tag}")

    session.flush()

    print("🤝 Connecting all users as peers...")
    for i, (u1, _) in enumerate(created):
        for j, (u2, _) in enumerate(created):
            if i >= j:
                continue
            peer = Peer()
            peer.user_id = u1.id
            peer.peer_id = u2.id
            peer.status = "accepted"
            session.add(peer)
    session.flush()

    print("🏋️  Creating workouts, posts, PRs, favorites, check-ins...")
    all_posts = []

    for user, persona in created:
        atype = persona["athlete_type"]

        # Favorites
        for fname in FAVORITES[atype]:
            f = FavoriteExercise()
            f.user_id = user.id
            f.name = fname
            session.add(f)

        # PRs
        for ex_name, weight, reps in PRS[atype]:
            pr = PR()
            pr.user_id = user.id
            pr.exercise_name = ex_name
            pr.weight = weight
            pr.reps = reps
            pr.date = ago(days=random.randint(3, 21)).date()
            session.add(pr)

        # Body metrics (last 6 entries)
        base_weight = {"powerlifter": 220, "hiit": 145, "athlete": 195, "runner": 155, "bodybuilder": 185}[atype]
        for week in range(6, 0, -1):
            bm = BodyMetric()
            bm.user_id = user.id
            bm.weight = base_weight + random.uniform(-2, 2)
            bm.recorded_at = ago(days=week * 7)
            session.add(bm)

        # Gym check-ins
        gym_name, gym_addr = random.choice(GYMS)
        for day in [1, 4, 8]:
            ci = GymCheckIn()
            ci.user_id = user.id
            ci.gym_name = gym_name
            ci.gym_address = gym_addr
            ci.checked_in_at = ago(days=day, hours=random.randint(6, 20))
            session.add(ci)

        # Workouts + workout posts
        for wi, (wname, wtype, wdur, exercises) in enumerate(WORKOUTS[atype]):
            w = Workout()
            w.user_id = user.id
            w.name = wname
            w.type = wtype
            w.duration = wdur
            w.is_public = True
            w.created_at = ago(days=wi * 3 + random.randint(0, 2))
            session.add(w)
            session.flush()

            for ex_name, sets_data in exercises:
                ex = Exercise()
                ex.name = ex_name
                ex.workout_id = w.id
                session.add(ex)
                session.flush()
                for weight, reps in sets_data:
                    s = Sets()
                    s.exercise_id = ex.id
                    s.weight = weight
                    s.reps = reps
                    session.add(s)

            wpost = Post()
            wpost.user_id = user.id
            wpost.workout_id = w.id
            wpost.text = f"Just finished {w.name} 💪"
            wpost.likes = random.randint(4, 18)
            wpost.date = w.created_at + timedelta(minutes=wdur + random.randint(10, 40))
            session.add(wpost)
            session.flush()
            all_posts.append(wpost)

        # Standalone text posts
        for pi, text in enumerate(POST_TEXTS[atype]):
            post = Post()
            post.user_id = user.id
            post.text = text
            post.likes = random.randint(6, 45)
            post.date = ago(days=pi + random.randint(0, 3), hours=random.randint(7, 22))
            session.add(post)
            session.flush()
            all_posts.append(post)

    session.flush()

    print("💬 Adding comments...")
    random.shuffle(all_posts)
    for post in all_posts[:30]:
        commenters = [u for u, _ in created if u.id != post.user_id]
        for commenter in random.sample(commenters, random.randint(1, 3)):
            c = Comment()
            c.post_id = post.id
            c.user_id = commenter.id
            c.text = random.choice(COMMENTS)
            c.date = post.date + timedelta(minutes=random.randint(5, 240))
            session.add(c)

    session.flush()

    print("\n✅ Demo seed complete!")
    print(f"   {len(PERSONAS)} users  |  {len(all_posts)} posts  |  comments, PRs, workouts, check-ins added")
    print("\n🎯 Demo login credentials:")
    print(f"   Email:    {DEMO_EMAIL}")
    print(f"   Password: {DEMO_PASSWORD}")
