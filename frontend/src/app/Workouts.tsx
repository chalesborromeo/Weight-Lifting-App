import { useEffect, useState } from "react";
import { Link } from "react-router";
import { workoutsApi } from "@/api";
import type { Workout } from "@/types";

export default function Workouts() {
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        setWorkouts(await workoutsApi.list());
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load workouts");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl tracking-tight">Workouts</h1>
        <Link
          to="/workouts/new"
          className="px-3 py-1 text-xs rounded-full bg-black text-white"
        >
          + New
        </Link>
      </div>

      {loading && <div className="text-sm text-black/60">Loading…</div>}
      {error && <div className="text-sm text-red-600">{error}</div>}
      {!loading && workouts.length === 0 && (
        <div className="text-sm text-black/60">No workouts yet.</div>
      )}

      <ul className="space-y-3">
        {workouts.map((w) => (
          <li key={w.id} className="border border-black/10 rounded-lg p-4">
            <div className="flex items-baseline justify-between">
              <div className="text-base">{w.name}</div>
              <div className="text-xs text-black/50">#{w.id}</div>
            </div>
            <div className="text-xs text-black/60 mt-1">
              {w.type} · {w.duration} min · {w.exercises.length} exercise(s)
            </div>
            {w.exercises.length > 0 && (
              <ul className="mt-3 space-y-1 text-xs text-black/70">
                {w.exercises.map((ex) => (
                  <li key={ex.id}>
                    <span className="text-black">{ex.name}</span>
                    <span className="text-black/50"> — {ex.sets.length} set(s)</span>
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
