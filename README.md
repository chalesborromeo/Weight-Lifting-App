# Spotter — Weight Lifting App

IT 326 Project App

Spotter is a social fitness platform for tracking workouts, personal records, and body metrics while connecting with gym peers, clubs, and spotters. It pairs a FastAPI backend with a React + TypeScript frontend.

## Features

- **Authentication** — register/login with JWT-based access and refresh tokens
- **Workouts** — log workouts and sets, view workout history
- **Personal Records (PRs)** — track and celebrate strength milestones
- **Body Metrics** — log weight, height, and body fat percentage over time, with goal tracking and charts
- **Social Feed & Posts** — share updates and progress with the community
- **Clubs** — create and join training clubs
- **Peers & Spotters** — connect with workout partners and send/accept spot requests
- **Gyms & Check-ins** — track gym locations and check-ins
- **Favorite Exercises & Suggested Workouts** — save go-to exercises and get workout suggestions
- **Notifications** — stay updated on social activity
- **Reports** — export data
- **Dark/light theme toggle**

## Tech Stack

**Backend**
- Python, FastAPI
- SQLAlchemy + Alembic (PostgreSQL)
- JWT auth (python-jose), password hashing (passlib/pwdlib)
- pytest for testing

**Frontend**
- React 18 + TypeScript, Vite
- React Router
- Tailwind CSS + shadcn/ui (Radix UI) components
- Recharts for data visualization
- Framer Motion (motion) for animations

## Project Structure

```
Weight-Lifting-App/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # FastAPI routers (auth, workouts, prs, clubs, etc.)
│   │   ├── core/             # config and security (JWT, hashing)
│   │   ├── db/                # DB connection, repository, factory abstractions
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # business logic
│   │   └── main.py            # FastAPI app entrypoint
│   ├── alembic/               # database migrations
│   ├── tests/                 # pytest test suite
│   ├── seed.py / seed_demo.py  # database seed scripts
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/                # typed API client functions
    │   ├── app/                 # page components/routes
    │   ├── components/          # shared UI components
    │   ├── context/             # React context (current user, theme)
    │   ├── types/                # shared TypeScript types
    │   └── main.tsx              # routes and app entrypoint
    └── package.json
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `backend/` directory with the following variables:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/weightlifting
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. (Optional) Seed the database with sample data:
   ```bash
   python seed.py
   # or
   python seed_demo.py
   ```

6. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`.

## Running Tests

Backend tests use pytest:

```bash
cd backend
pytest
```

## Linting

```bash
cd frontend
npm run lint
```

## License

This project was created for IT 326.
