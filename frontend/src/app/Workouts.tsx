import { useEffect, useState } from "react";
import { workoutsApi } from "@/api";
import type { Workout } from "@/types";
import { SectionHeader } from "@/components/SectionHeader";

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
      <SectionHeader title="Workouts" />

      {loading && <div className="text-sm text-muted-foreground">Loading...</div>}
      {error && <div className="text-sm text-destructive">{error}</div>}
      {!loading && workouts.length === 0 && (
        <div className="bg-card rounded-[20px] p-8 text-center">
          <p className="text-sm text-muted-foreground">No workouts yet.</p>
        </div>
      )}

      <div className="space-y-3">
        {workouts.map((w) => (
          <div key={w.id} className="bg-card rounded-[20px] p-4">
            <div className="flex items-baseline justify-between">
              <div className="text-base font-semibold text-foreground">{w.name}</div>
              <span className="text-xs bg-accent/10 text-accent px-2.5 py-1 rounded-[15px]">
                {w.type}
              </span>
            </div>
            <div className="text-xs text-muted-foreground mt-1">
              {w.duration} min · {w.exercises.length} exercise(s)
            </div>
            {w.exercises.length > 0 && (
              <ul className="mt-3 space-y-1 text-xs">
                {w.exercises.map((ex) => (
                  <li key={ex.id}>
                    <span className="text-foreground">{ex.name}</span>
                    <span className="text-muted-foreground"> — {ex.sets.length} set(s)</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
