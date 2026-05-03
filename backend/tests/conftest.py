import pytest
from fastapi.testclient import TestClient

# Import ALL models so SQLAlchemy can resolve all relationships before any test runs.
import app.models.user
import app.models.workout
import app.models.post
import app.models.comment
import app.models.peer
import app.models.profile
import app.models.pr
import app.models.gym
import app.models.gym_checkin
import app.models.body_metric
import app.models.favorite_exercise
import app.models.notification
import app.models.report
import app.models.spot_Request
import app.models.club
import app.models.exercise
import app.models.sets

from app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
