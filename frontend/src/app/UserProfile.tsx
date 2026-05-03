import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { usersApi } from "@/api/users";
import { workoutsApi } from "@/api/workouts";
import { SectionHeader } from "@/components/SectionHeader";
import type { User, Workout } from "@/types";

function formatDuration(mins: number): string {
  const h = Math.floor(mins / 60);
  const m = Math.round(mins % 60);
  return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

function timeAgo(dateStr: string): string {
  const seconds = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000);
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days}d ago`;
  return new Date(dateStr).toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function getDisplayName(user: User): string {
  const name = [user.first_name, user.last_name].filter(Boolean).join(" ");
  return name || user.email;
}

export default function UserProfile() {
  const { id } = useParams<{ id: string }>();
  const userId = Number(id);

  const [user, setUser] = useState<User | null>(null);
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;
    (async () => {
      try {
        const [u, ws] = await Promise.all([
          usersApi.get(userId),
          workoutsApi.listByUser(userId),
        ]);
        setUser(u);
        setWorkouts(ws);
      } catch {
        setError("Could not load this profile.");
      } finally {
        setLoading(false);
      }
    })();
  }, [userId]);

  if (loading) {
    return (
      <div className="space-y-6">
        <SectionHeader title="Profile" />
        <div className="bg-card rounded-[20px] p-8 text-center">
          <p className="text-sm text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (error || !user) {
    return (
      <div className="space-y-6">
        <SectionHeader title="Profile" />
        <div className="bg-card rounded-[20px] p-8 text-center">
          <p className="text-sm text-destructive">{error ?? "User not found."}</p>
        </div>
      </div>
    );
  }

  const displayName = getDisplayName(user);
  const initial = user.email.charAt(0).toUpperCase();
  const totalSets = workouts.reduce(
    (sum, w) => sum + w.exercises.reduce((s, e) => s + e.sets.length, 0),
    0
  );

  return (
    <div className="space-y-6">
      <SectionHeader title="Profile" />

      {/* Identity card */}
      <div className="bg-card rounded-[20px] p-5 flex items-center gap-4">
        <div className="w-16 h-16 rounded-[15px] bg-accent flex items-center justify-center text-white text-2xl font-bold shrink-0">
          {initial}
        </div>
        <div className="min-w-0 flex-1">
          <div className="text-lg font-semibold text-foreground truncate">{displayName}</div>
          <div className="text-xs text-muted-foreground truncate">{user.email}</div>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-card rounded-[16px] p-4 text-center">
          <div className="text-2xl font-bold text-foreground">{workouts.length}</div>
          <div className="text-xs text-muted-foreground mt-0.5 uppercase tracking-wide">Workouts</div>
        </div>
        <div className="bg-card rounded-[16px] p-4 text-center">
          <div className="text-2xl font-bold text-foreground">{totalSets}</div>
          <div className="text-xs text-muted-foreground mt-0.5 uppercase tracking-wide">Total Sets</div>
        </div>
      </div>

      {/* Recent workouts */}
      <div className="space-y-2">
        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide px-1">
          Recent Workouts
        </p>
        {workouts.length === 0 && (
          <div className="bg-card rounded-[20px] p-8 text-center">
            <p className="text-sm text-muted-foreground">No workouts yet.</p>
          </div>
        )}
        {workouts.slice(0, 10).map((w) => (
          <div key={w.id} className="bg-card rounded-[16px] px-4 py-3 flex items-center gap-3">
            <div className="flex-1 min-w-0">
              <div className="text-sm font-semibold text-foreground truncate">{w.name}</div>
              <div className="text-xs text-muted-foreground mt-0.5">
                {w.exercises.length} exercises · {formatDuration(w.duration)}
              </div>
            </div>
            <span className="text-xs text-accent bg-accent/10 px-2.5 py-1 rounded-full uppercase tracking-wide shrink-0">
              {w.type}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
