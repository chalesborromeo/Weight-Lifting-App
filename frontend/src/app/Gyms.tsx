import { useEffect, useState } from "react";
import { MapPin, Star, Clock, Navigation, LogIn, Trash2 } from "lucide-react";
import { gymsApi } from "@/api";
import { SectionHeader } from "@/components/SectionHeader";
import type { GymCheckIn, NearbyGym } from "@/types";

const RADIUS_OPTIONS = [5, 10, 25, 50];

function fmtDistance(km: number): string {
  if (km < 1) return `${Math.round(km * 1000)} m`;
  return `${km.toFixed(1)} km`;
}

function fmtHours(open?: string | null, close?: string | null): string | null {
  if (!open && !close) return null;
  const parts = [open, close].filter(Boolean);
  return parts.join(" – ");
}

function fmtDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, {
    month: "short", day: "numeric", year: "numeric",
    hour: "numeric", minute: "2-digit",
  });
}

export default function Gyms() {
  const [gyms, setGyms] = useState<NearbyGym[]>([]);
  const [radius, setRadius] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState(false);
  const [checkins, setCheckins] = useState<GymCheckIn[]>([]);

  useEffect(() => {
    gymsApi.listCheckins().then(setCheckins).catch(() => setCheckins([]));
  }, []);

  const findNearby = () => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by your browser.");
      return;
    }
    setLoading(true);
    setError(null);
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          const results = await gymsApi.nearby(
            pos.coords.latitude,
            pos.coords.longitude,
            radius,
          );
          setGyms(results);
          setSearched(true);
        } catch (err) {
          setError(err instanceof Error ? err.message : "Failed to fetch nearby gyms.");
        } finally {
          setLoading(false);
        }
      },
      () => {
        setError("Location access denied. Enable location permissions and try again.");
        setLoading(false);
      },
      { maximumAge: 60_000, timeout: 10_000 },
    );
  };

  const handleCheckIn = async (gym: NearbyGym) => {
    const newCheckin = await gymsApi.checkin(gym.name, gym.address ?? null);
    setCheckins((prev) => [newCheckin, ...prev]);
  };

  const handleDeleteCheckin = async (id: number) => {
    await gymsApi.deleteCheckin(id);
    setCheckins((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <div className="space-y-6">
      <SectionHeader title="Nearby Gyms" />

      <div className="bg-card rounded-[20px] p-4 space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm text-foreground">Search radius</span>
          <div className="flex gap-2">
            {RADIUS_OPTIONS.map((r) => (
              <button
                key={r}
                onClick={() => setRadius(r)}
                className={`px-3 py-1 rounded-full text-xs transition-colors ${
                  radius === r
                    ? "bg-accent text-white"
                    : "bg-background text-muted-foreground hover:text-foreground"
                }`}
              >
                {r} km
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={findNearby}
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 bg-accent text-white px-4 py-3 rounded-[15px] active:scale-95 transition-transform disabled:opacity-50"
        >
          <Navigation className="w-4 h-4" />
          {loading ? "Locating..." : "Find Gyms Near Me"}
        </button>
      </div>

      {error && (
        <div className="bg-destructive/10 rounded-[20px] p-4 text-sm text-destructive text-center">
          {error}
        </div>
      )}

      {searched && !loading && gyms.length === 0 && !error && (
        <div className="bg-card rounded-[20px] p-8 text-center text-sm text-muted-foreground">
          No gyms found within {radius} km.
        </div>
      )}

      {gyms.length > 0 && (
        <div className="space-y-3">
          <p className="text-xs text-muted-foreground uppercase tracking-wide">
            {gyms.length} gym{gyms.length !== 1 ? "s" : ""} within {radius} km
          </p>
          {gyms.map((gym) => (
            <GymCard key={gym.id} gym={gym} onCheckIn={() => handleCheckIn(gym)} />
          ))}
        </div>
      )}

      {checkins.length > 0 && (
        <div className="space-y-3">
          <h2 className="text-xs uppercase tracking-wide text-muted-foreground">My Check-ins</h2>
          {checkins.map((c) => (
            <div key={c.id} className="bg-card rounded-[16px] px-4 py-3 flex items-center gap-3">
              <LogIn className="w-4 h-4 text-accent shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground truncate">{c.gym_name}</p>
                {c.gym_address && (
                  <p className="text-xs text-muted-foreground truncate">{c.gym_address}</p>
                )}
                <p className="text-xs text-muted-foreground">{fmtDate(c.checked_in_at)}</p>
              </div>
              <button
                onClick={() => handleDeleteCheckin(c.id)}
                className="text-muted-foreground hover:text-destructive transition-colors"
                title="Remove check-in"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function GymCard({ gym, onCheckIn }: { gym: NearbyGym; onCheckIn: () => void }) {
  const hours = fmtHours(gym.hours_open, gym.hours_close);
  const [checkedIn, setCheckedIn] = useState(false);

  const handleCheckIn = () => {
    onCheckIn();
    setCheckedIn(true);
    setTimeout(() => setCheckedIn(false), 3000);
  };

  return (
    <div className="bg-card rounded-[20px] p-4 space-y-3">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <h3 className="text-base font-semibold text-foreground truncate">{gym.name}</h3>
          {gym.address && (
            <p className="text-sm text-muted-foreground mt-0.5 truncate">{gym.address}</p>
          )}
        </div>
        <span className="shrink-0 text-sm font-medium text-accent bg-accent/10 px-2.5 py-1 rounded-full whitespace-nowrap">
          {fmtDistance(gym.distance_km)}
        </span>
      </div>

      <div className="flex flex-wrap gap-3 text-xs text-muted-foreground">
        {gym.rating != null && (
          <span className="flex items-center gap-1">
            <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
            {gym.rating.toFixed(1)}
          </span>
        )}
        {hours && (
          <span className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" />
            {hours}
          </span>
        )}
        <span className="flex items-center gap-1">
          <MapPin className="w-3.5 h-3.5" />
          {gym.latitude.toFixed(4)}, {gym.longitude.toFixed(4)}
        </span>
      </div>

      <button
        onClick={handleCheckIn}
        className={`w-full flex items-center justify-center gap-2 py-2 rounded-[12px] text-sm transition-colors ${
          checkedIn
            ? "bg-green-500/20 text-green-600"
            : "bg-accent/10 text-accent hover:bg-accent/20"
        }`}
      >
        <LogIn className="w-4 h-4" />
        {checkedIn ? "Checked in!" : "Check In"}
      </button>
    </div>
  );
}
