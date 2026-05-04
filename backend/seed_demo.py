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
from app.models.club import Club
from pwdlib import PasswordHash
from datetime import datetime, timedelta, date
import sqlalchemy as sa
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
        "first_name": "Kobe",
        "last_name": "Bryant",
        "bio": "junior @ ISU. been lifting since freshman year, mostly powerlifting stuff",
        "athlete_type": "powerlifter",
        "is_demo": True,
    },
    {
        "email": "lebron.j@spotter.app",
        "password": "password123",
        "first_name": "LeBron",
        "last_name": "James",
        "bio": "cs major. hit the rec center between classes when i can",
        "athlete_type": "powerlifter",
    },
    {
        "email": "steph.c@spotter.app",
        "password": "password123",
        "first_name": "Stephen",
        "last_name": "Curry",
        "bio": "kinesiology sophomore. teach a hiit class fri mornings at the rec",
        "athlete_type": "hiit",
    },
    {
        "email": "magic.j@spotter.app",
        "password": "password123",
        "first_name": "Magic",
        "last_name": "Johnson",
        "bio": "on the track team. trying to get my lifts up during the off season",
        "athlete_type": "athlete",
    },
    {
        "email": "allen.i@spotter.app",
        "password": "password123",
        "first_name": "Allen",
        "last_name": "Iverson",
        "bio": "nursing student. started lifting to cross train for half marathons",
        "athlete_type": "runner",
    },
    {
        "email": "shaq.oneal@spotter.app",
        "password": "password123",
        "first_name": "Shaquille",
        "last_name": "O'Neal",
        "bio": "senior. doing my first show in april, logging everything until then",
        "athlete_type": "bodybuilder",
    },
]

WORKOUTS = {
    "powerlifter": [
        ("Squat Day", "Strength", 90, [
            ("Back Squat", [(315, 5), (335, 3), (355, 1)]),
            ("Romanian Deadlift", [(225, 8), (225, 8)]),
            ("Leg Press", [(450, 10), (450, 10)]),
        ]),
        ("Pull Day", "Strength", 75, [
            ("Deadlift", [(405, 3), (455, 1), (495, 1)]),
            ("Barbell Row", [(185, 8), (185, 8), (185, 8)]),
            ("Pull-Ups", [(0, 10), (0, 8)]),
        ]),
        ("Bench Day", "Strength", 60, [
            ("Bench Press", [(225, 5), (245, 3), (265, 1)]),
            ("Incline Dumbbell Press", [(85, 8), (85, 8)]),
            ("Tricep Pushdown", [(70, 12), (70, 12)]),
        ]),
    ],
    "hiit": [
        ("Morning Circuit", "HIIT", 40, [
            ("Burpees", [(0, 20), (0, 20), (0, 20)]),
            ("Box Jumps", [(0, 15), (0, 15)]),
            ("Kettlebell Swings", [(35, 20), (35, 20)]),
        ]),
        ("Full Body", "HIIT", 45, [
            ("Jump Squats", [(0, 15), (0, 15), (0, 15)]),
            ("Push-Ups", [(0, 25), (0, 25)]),
            ("Mountain Climbers", [(0, 30), (0, 30)]),
        ]),
    ],
    "athlete": [
        ("Speed and Power", "Strength", 70, [
            ("Power Clean", [(135, 5), (155, 4), (175, 3)]),
            ("Box Squat", [(275, 5), (275, 5)]),
            ("Broad Jump", [(0, 5), (0, 5)]),
        ]),
        ("Upper Body", "Strength", 55, [
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
        ("Core Work", "Strength", 35, [
            ("Plank", [(0, 60), (0, 60)]),
            ("Dead Bug", [(0, 10), (0, 10)]),
            ("Cable Woodchop", [(40, 12), (40, 12)]),
        ]),
    ],
    "bodybuilder": [
        ("Chest and Triceps", "Bodybuilding", 75, [
            ("Bench Press", [(185, 10), (185, 10), (185, 10)]),
            ("Cable Fly", [(50, 15), (50, 15), (50, 15)]),
            ("Skull Crushers", [(75, 12), (75, 12), (75, 12)]),
        ]),
        ("Back and Biceps", "Bodybuilding", 70, [
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
        "495 actually moved today. been stuck at 475 for like 3 weeks so this was needed",
        "355 squat felt way easier than it should have. maybe finally turned a corner",
        "rest day. my back is cooked from yesterday honestly",
        "hit all 3 openers at the meet today. first time that's happened lol",
        "bench finally went up. slow but at least its moving",
    ],
    "hiit": [
        "new circuit kicked my ass this morning and i have an exam at 11. great combo",
        "teaching the friday class tomorrow, updated the intervals. we'll see how it goes",
        "just stretched and rolled out today, legs were dead from tuesday",
        "needed that session. had a rough week and just needed to move",
        "had to modify the whole circuit for someone mid-class. improvised it on the spot",
    ],
    "athlete": [
        "185 on the power clean for 3. that's a pr, bar felt fast",
        "morning speed work then lifted after practice. tired but good tired",
        "nobody sees the off-season work and that's honestly fine",
        "got to the weight room before anyone else today. love when that happens",
        "catch position on the clean finally started making sense. took long enough",
    ],
    "runner": [
        "ran 8 miles then did legs. probably dumb but felt okay somehow",
        "been lifting for 6 months and my mile time actually dropped. didn't expect that",
        "trying to hit sub 7 and 135lb goblet squat by end of the month. both feel close",
        "used to cramp up bad at mile 18. added calf work and it hasn't happened since",
        "core stuff is so boring but my knees haven't hurt in months so whatever",
    ],
    "bodybuilder": [
        "12 weeks out. just staying consistent at this point",
        "back and bis today. rows felt really good",
        "one of those sessions where everything just clicks. rare but nice",
        "starting carb cycling this week. a little nervous about energy during lifts",
        "posing practice at 10pm after a full day of class. prep is no joke",
    ],
}

COMMENTS = [
    "bro nice",
    "lets go",
    "that's crazy",
    "ok that's actually impressive",
    "i need to get back in the gym",
    "been meaning to try that",
    "how long did that take",
    "W",
    "that's a big number",
    "rest days are so underrated",
    "ok i felt that",
    "that sounds awful lol",
    "yoo good work",
    "same honestly",
    "what weight were you using",
    "teach me",
    "inspirational fr",
    "this is making me want to go tonight",
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

ISU_CLUBS = [
    {
        "name": "ISU Powerlifting Club",
        "description": "Competing and training powerlifters at Illinois State. Open to all skill levels. We run a meet every semester.",
        "privacy": "public",
        "owner_type": "powerlifter",
        "member_types": ["powerlifter", "athlete", "bodybuilder"],
    },
    {
        "name": "Redbird Running Crew",
        "description": "Casual running group for ISU students. Weekly group runs on the quad, half marathon training every spring.",
        "privacy": "public",
        "owner_type": "runner",
        "member_types": ["runner", "hiit", "athlete"],
    },
    {
        "name": "ISU Rec Center HIIT Class",
        "description": "Official HIIT group at the ISU Rec Center. Classes run Mon/Wed/Fri at 6am and 5pm. All fitness levels welcome.",
        "privacy": "public",
        "owner_type": "hiit",
        "member_types": ["hiit", "runner", "athlete"],
    },
    {
        "name": "Redbird Bodybuilding",
        "description": "ISU students focused on physique and competition prep. Sharing programs, check-ins, and stage prep tips.",
        "privacy": "public",
        "owner_type": "bodybuilder",
        "member_types": ["bodybuilder", "powerlifter"],
    },
    {
        "name": "ISU Strength & Conditioning",
        "description": "For student athletes and anyone training like one. Heavy compound lifts, speed work, and sport-specific programming.",
        "privacy": "public",
        "owner_type": "athlete",
        "member_types": ["athlete", "powerlifter", "bodybuilder"],
    },
]


def ago(days=0, hours=0):
    return datetime.now() - timedelta(days=days, hours=hours)


with conn.get_session() as session:
    print("🧹 Clearing old demo data...")
    # Delete everyone — demo users get re-created fresh each run
    all_users = session.query(User).all()
    all_ids = [u.id for u in all_users]
    if all_ids:
        id_list = ", ".join(str(i) for i in all_ids)
        session.execute(sa.text(f"DELETE FROM spot_requests WHERE requester_id IN ({id_list}) OR spotter_id IN ({id_list})"))
        session.execute(sa.text(f"DELETE FROM peers WHERE user_id IN ({id_list}) OR peer_id IN ({id_list})"))
        session.flush()
        for u in all_users:
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

        # Body metrics (12 weekly entries with realistic trend)
        base_weight = {"powerlifter": 220, "hiit": 145, "athlete": 195, "runner": 155, "bodybuilder": 185}[atype]
        base_height = {"powerlifter": 71, "hiit": 65, "athlete": 73, "runner": 66, "bodybuilder": 70}[atype]
        base_bf    = {"powerlifter": 18, "hiit": 16, "athlete": 14, "runner": 13, "bodybuilder": 11}[atype]
        trend = {"powerlifter": -0.3, "hiit": -0.2, "athlete": 0.1, "runner": -0.15, "bodybuilder": -0.4}[atype]
        for week in range(12, 0, -1):
            bm = BodyMetric()
            bm.user_id = user.id
            bm.weight = round(base_weight + trend * (12 - week) + random.uniform(-0.5, 0.5), 1)
            bm.height = base_height
            bm.body_fat_pct = round(base_bf + (trend * 0.1) * (12 - week) + random.uniform(-0.3, 0.3), 1)
            bm.date = ago(days=week * 7)
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

    print("🏫 Creating ISU clubs...")
    user_by_type = {persona["athlete_type"]: user for user, persona in created}
    for club_def in ISU_CLUBS:
        club = Club()
        club.name = club_def["name"]
        club.description = club_def["description"]
        club.privacy = club_def["privacy"]
        club.owner_id = user_by_type[club_def["owner_type"]].id
        session.add(club)
        session.flush()
        for atype in club_def["member_types"]:
            if atype in user_by_type:
                club.members.append(user_by_type[atype])
    session.flush()

    print("\n✅ Demo seed complete!")
    print(f"   {len(PERSONAS)} users  |  {len(all_posts)} posts  |  {len(ISU_CLUBS)} clubs  |  comments, PRs, workouts, check-ins added")
    print("\n🎯 Demo login credentials:")
    print(f"   Email:    {DEMO_EMAIL}")
    print(f"   Password: {DEMO_PASSWORD}")
