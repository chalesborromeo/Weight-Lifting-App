import { useEffect, useState } from "react";
import { statsApi } from "@/api";
import type { WorkoutStats, PeriodicVolume } from "@/types";

type Range = "week" | "month" | "year";

function getRange(r: Range): { start: Date; end: Date } {
  const end = new Date();
  const start = new Date();
  if (r === "week") start.setDate(end.getDate() - 7);
  else if (r === "month") start.setMonth(end.getMonth() - 1);
  else start.setFullYear(end.getFullYear() - 1);
  return { start, end };
}

export default function Stats() {
  const [range, setRange] = useState<Range>("month");
  const [stats, setStats] = useState<WorkoutStats | null>(null);
  const [periodic, setPeriodic] = useState<PeriodicVolume[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    setError("");
    const { start, end } = getRange(range);
    Promise.all([statsApi.overview(start, end), statsApi.periodic(start, end)])
      .then(([s, p]) => {
        setStats(s);
        setPeriodic(p);
      })
      .catch(() => setError("Failed to load stats."))
      .finally(() => setLoading(false));
  }, [range]);

  const maxVolume = Math.max(...periodic.map((p) => p.total_volume), 1);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Stats</h1>
        <div className="flex gap-1 bg-card rounded-[12px] p-1">
          {(["week", "month", "year"] as Range[]).map((r) => (
            <button
              key={r}
              onClick={() => setRange(r)}
              className={`px-3 py-1.5 text-sm rounded-[10px] capitalize transition-colors ${
                range === r
                  ? "bg-accent text-white"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {r}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <p className="text-muted-foreground text-sm text-center py-8">Loading...</p>
      )}
      {error && (
        <p className="text-destructive text-sm text-center py-8">{error}</p>
      )}

      {!loading && !error && stats && (
        <>
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: "Workouts", value: stats.volume.total_workouts },
              { label: "PRs", value: stats.pr_count },
              { label: "Total Sets", value: stats.volume.total_sets },
              { label: "Total Reps", value: stats.volume.total_reps },
            ].map((s) => (
              <div key={s.label} className="bg-card rounded-[16px] p-4 space-y-1">
                <div className="text-2xl font-bold">{s.value}</div>
                <div className="text-xs text-muted-foreground">{s.label}</div>
              </div>
            ))}
          </div>

          <div className="bg-card rounded-[16px] p-4 space-y-1">
            <div className="text-2xl font-bold">
              {stats.volume.total_volume.toLocaleString()} lbs
            </div>
            <div className="text-xs text-muted-foreground">Total Volume Lifted</div>
          </div>

          {periodic.length > 0 && (
            <div className="bg-card rounded-[16px] p-4 space-y-3">
              <h2 className="text-sm font-semibold">Volume by Week</h2>
              <div className="flex items-end gap-1.5" style={{ height: 128 }}>
                {periodic.map((p) => (
                  <div
                    key={p.period_start}
                    className="flex-1 flex flex-col items-center justify-end gap-1"
                  >
                    <div
                      className="w-full bg-accent/80 rounded-t-[4px]"
                      style={{ height: Math.max(4, (p.total_volume / maxVolume) * 96) }}
                    />
                    <span className="text-[9px] text-muted-foreground leading-none">
                      {new Date(p.period_start).toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                      })}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {stats.prs.length > 0 && (
            <div className="space-y-2">
              <h2 className="text-sm font-semibold">Recent PRs</h2>
              {stats.prs.map((pr) => (
                <div
                  key={pr.id}
                  className="bg-card rounded-[16px] p-4 flex items-center justify-between"
                >
                  <span className="text-sm font-medium">{pr.exercise_name}</span>
                  <span className="text-sm text-muted-foreground">
                    {pr.weight} kg × {pr.reps}
                  </span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
