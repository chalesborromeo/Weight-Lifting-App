import math
import time

import httpx
from fastapi import HTTPException, status

from app.db.repositories import DBRepository
from app.models.gym import Gym
from app.schemas.gym import GymCreate

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_TIMEOUT = 15  # seconds

# In-memory cache: key → (timestamp, results)
# Keyed by (lat_1dp, lon_1dp, radius_km) — 1 decimal place ≈ 11 km grid, good enough
# to share results for users in the same area.
_cache: dict[tuple, tuple[float, list]] = {}
CACHE_TTL = 300  # seconds (5 minutes)


def _cache_key(lat: float, lon: float, radius_km: float) -> tuple:
    return (round(lat, 1), round(lon, 1), radius_km)


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _build_address(tags: dict) -> str | None:
    parts = [
        tags.get("addr:housenumber", ""),
        tags.get("addr:street", ""),
        tags.get("addr:city", ""),
    ]
    address = " ".join(p for p in parts if p).strip()
    return address or tags.get("addr:full") or None


def _fetch_overpass(lat: float, lon: float, radius_m: int) -> list[dict]:
    # Nodes only — ways add significant overhead and most gyms are nodes.
    query = f"""
[out:json][timeout:{OVERPASS_TIMEOUT}];
node["leisure"="fitness_centre"](around:{radius_m},{lat},{lon});
out body;
"""
    try:
        resp = httpx.post(
            OVERPASS_URL,
            data={"data": query},
            headers={"User-Agent": "spotter-app/1.0"},
            timeout=OVERPASS_TIMEOUT,
        )
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Overpass API error: {exc}",
        )

    results = []
    for i, el in enumerate(resp.json().get("elements", []), start=1):
        tags = el.get("tags", {})
        name = tags.get("name") or tags.get("brand") or "Unnamed Gym"
        results.append({
            "id": i,
            "name": name,
            "address": _build_address(tags),
            "latitude": el["lat"],
            "longitude": el["lon"],
            "hours_open": None,
            "hours_close": None,
            "rating": None,
        })

    return results


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
        key = _cache_key(latitude, longitude, radius_km)
        cached_at, cached_gyms = _cache.get(key, (0.0, []))

        if time.monotonic() - cached_at < CACHE_TTL:
            gyms = cached_gyms
        else:
            gyms = _fetch_overpass(latitude, longitude, int(radius_km * 1000))
            _cache[key] = (time.monotonic(), gyms)

        results = [
            {**g, "distance_km": round(_haversine_km(latitude, longitude, g["latitude"], g["longitude"]), 3)}
            for g in gyms
        ]
        results.sort(key=lambda g: g["distance_km"])
        return results
