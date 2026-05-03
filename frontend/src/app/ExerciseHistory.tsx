import { useEffect, useMemo, useState } from "react";
import { workoutsApi } from "@/api/workouts";
import { statsApi } from "@/api/stats";
import { useCurrentUser } from "@/context/CurrentUser";
import { SectionHeader } from "@/components/SectionHeader";
import type { Workout, PRProgression } from "@/types";

function formatDate(d: string | Date): string {
  return new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

export default function ExerciseHistory() {
  const { userId } = useCurrentUser();
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [loadingWorkouts, setLoadingWorkouts] = useState(true);
  const [selected, setSelected] = useState<string>("");
  const [progression, setProgression] = useState<PRProgression | null>(null);
  const [loadingProg, setLoadingProg] = useState(false);

  useEffect(() => {
    if (!userId) return;
    workoutsApi.listByUser(userId)
      .then((ws) => { setWorkouts(ws); })
      .finally(() => setLoadingWorkouts(false));
  }, [userId]);

  const exerciseNames = useMemo(() => {
    const names = new Set<string>();
    for (const w of workouts) {
      for (const e of w.exercises) names.add(e.name);
    }
    return Array.from(names).sort();
  }, [workouts]);

  useEffect(() => {
    if (!selected) { setProgression(null); return; }
    setLoadingProg(true);
    const end = new Date();
    const start = new Date();
    start.setFullYear(end.getFullYear() - 1);
    statsApi.progression(selected, start, end)
      .then(setProgression)
      .catch(() => setProgression(null))
      .finally(() => setLoadingProg(false));
  }, [selected]);

  // Sessions containing the selected exercise
  const sessions = useMemo(() => {
    if (!selected) return [];
    return workouts
      .filter((w) => w.exercises.some((e) => e.name === selected))
      .map((w) => ({
        workout: w,
        exercise: w.exercises.find((e) => e.name === selected)!,
      }))
      .sort((a, b) => {
        const da = (a.workout as unknown as { created_at?: string }).created_at ?? "";
        const db = (b.workout as unknown as { created_at?: string }).created_at ?? "";
        return db.localeCompare(da);
      });
  }, [workouts, selected]);

  const maxWeight = useMemo(
    () => Math.max(...sessions.flatMap((s) => s.exercise.sets.map((set) => set.weight)), 1),
    [sessions]
  );

  return (
    <div className="space-y-6">
      <SectionHeader title="Exercise History" />

      {loadingWorkouts ? (
        <div className="bg-card rounded-[20px] p-8 text-center">
          <p className="text-sm text-muted-foreground">Loading your workouts...</p>
        </div>
      ) : exerciseNames.length === 0 ? (
        <div className="bg-card rounded-[20px] p-8 text-center">
          <p className="text-sm text-muted-foreground">Log some workouts to see exercise history.</p>
        </div>
      ) : (
        <div className="bg-card rounded-[20px] p-4">
          <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wide block mb-2">
            Select Exercise
          </label>
          <select
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
            className="w-full px-3 py-2.5 text-sm bg-background rounded-[12px] outline-none focus:ring-1 focus:ring-accent transition-colors"
          >
            <option value="">— choose an exercise —</option>
            {exerciseNames.map((name) => (
              <option key={name} value={name}>{name}</option>
            ))}
          </select>
        </div>
      )}

      {selected && (
        <>
          {/* PR Progression */}
          {loadingProg ? (
            <div className="bg-card rounded-[20px] p-6 text-center">
              <p className="text-sm text-muted-foreground">Loading progression...</p>
            </div>
          ) : progression && progression.prs.length > 0 ? (
            <div className="bg-card rounded-[20px] p-4 space-y-3">
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                PR Progression
              </h3>
              <div className="space-y-2">
                {progression.prs.map((pr) => (
                  <div key={pr.id} className="flex items-center justify-between py-2 border-b border-border last:border-0">
                    <div>
                      <span className="text-sm font-semibold text-foreground">{pr.weight} lbs</span>
                      <span className="text-xs text-muted-foreground ml-1">× {pr.reps} reps</span>
                    </div>
                    <span className="text-xs text-muted-foreground">{formatDate(pr.date)}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : null}

          {/* Session history */}
          <div className="space-y-3">
            <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide px-1">
              Past Sessions ({sessions.length})
            </p>
            {sessions.length === 0 ? (
              <div className="bg-card rounded-[20px] p-8 text-center">
                <p className="text-sm text-muted-foreground">No sessions found for this exercise.</p>
              </div>
            ) : (
              sessions.map(({ workout, exercise }) => {
                const best = Math.max(...exercise.sets.map((s) => s.weight));
                return (
                  <div key={workout.id} className="bg-card rounded-[20px] p-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-foreground">{workout.name}</span>
                      <span className="text-xs text-muted-foreground">
                        {(workout as unknown as { created_at?: string }).created_at
                          ? formatDate((workout as unknown as { created_at: string }).created_at)
                          : ""}
                      </span>
                    </div>

                    {/* Mini bar chart */}
                    <div className="flex items-end gap-1.5 h-10">
                      {exercise.sets.map((set, i) => (
                        <div
                          key={i}
                          className="flex-1 bg-accent/70 rounded-t-[3px] relative group"
                          style={{ height: `${(set.weight / maxWeight) * 100}%`, minHeight: "4px" }}
                        >
                          <div className="absolute -top-7 left-1/2 -translate-x-1/2 bg-card border border-border text-[10px] px-1.5 py-0.5 rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                            {set.weight} lbs × {set.reps}
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>{exercise.sets.length} sets</span>
                      <span>Best: <span className="text-foreground font-medium">{best} lbs</span></span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </>
      )}
    </div>
  );
}
