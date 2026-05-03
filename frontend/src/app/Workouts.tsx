import { useEffect, useState } from "react";
import { Link } from "react-router";
import { workoutsApi } from "@/api";
import { useCurrentUser } from "@/context/CurrentUser";
import type { Workout } from "@/types";
import { SectionHeader } from "@/components/SectionHeader";

function formatDate(d: string): string {
  return new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

export default function Workouts() {
  const { userId } = useCurrentUser();
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;
    (async () => {
      try {
        setWorkouts(await workoutsApi.listByUser(userId));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load workouts");
      } finally {
        setLoading(false);
      }
    })();
  }, [userId]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <SectionHeader title="Workouts" />
        <Link
          to="/workouts/new"
          className="text-xs px-3 py-1.5 bg-accent text-white rounded-full hover:bg-accent/90 transition-colors"
        >
          + New
        </Link>
      </div>

      {loading && <div className="text-sm text-muted-foreground">Loading...</div>}
      {error && <div className="text-sm text-destructive">{error}</div>}
      {!loading && workouts.length === 0 && (
        <div className="bg-card rounded-[20px] p-8 text-center space-y-3">
          <p className="text-sm text-muted-foreground">No workouts yet.</p>
          <Link to="/workouts/new" className="text-sm text-accent hover:underline">Log your first workout →</Link>
        </div>
      )}

      <div className="space-y-3">
        {workouts.map((w) => (
          <div key={w.id} className="bg-card rounded-[20px] p-4">
            <div className="flex items-start justify-between gap-2">
              <div className="min-w-0">
                <div className="text-base font-semibold text-foreground truncate">{w.name}</div>
                <div className="text-xs text-muted-foreground mt-0.5">
                  {w.duration} min · {w.exercises.length} exercise(s)
                  {w.created_at && <> · {formatDate(w.created_at)}</>}
                  {w.is_public === false && <span className="ml-1.5 text-muted-foreground">🔒 Private</span>}
                </div>
              </div>
              <span className="text-xs bg-accent/10 text-accent px-2.5 py-1 rounded-full shrink-0">
                {w.type}
              </span>
            </div>
            {w.exercises.length > 0 && (
              <ul className="mt-3 space-y-1 text-xs border-t border-border pt-3">
                {w.exercises.map((ex) => (
                  <li key={ex.id} className="flex items-center justify-between">
                    <span className="text-foreground">{ex.name}</span>
                    <span className="text-muted-foreground">{ex.sets.length} set(s)</span>
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
