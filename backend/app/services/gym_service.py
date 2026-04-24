import math

from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.models.gym import Gym
from app.schemas.gym import GymCreate


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Earth radius in km; Haversine gives great-circle distance.
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


class GymService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def list_all(self):
        return self.repo.get_all_gyms(self.session)

    def get(self, gym_id: int):
        gym = self.repo.get_gym(gym_id, self.session)
        if not gym:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found")
        return gym

    def create(self, data: GymCreate):
        gym = Gym(**data.model_dump())
        self.repo.save_gym(gym, self.session)
        self.session.refresh(gym)
        return gym

    def list_nearby(self, latitude: float, longitude: float, radius_km: float):
        gyms = self.repo.get_all_gyms(self.session)
        results = []
        for g in gyms:
            d = _haversine_km(latitude, longitude, g.latitude, g.longitude)
            if d <= radius_km:
                results.append((g, d))
        results.sort(key=lambda pair: pair[1])
        return [
            {
                "id": g.id,
                "name": g.name,
                "address": g.address,
                "latitude": g.latitude,
                "longitude": g.longitude,
                "hours_open": g.hours_open,
                "hours_close": g.hours_close,
                "rating": g.rating,
                "distance_km": round(d, 3),
            }
            for g, d in results
        ]
