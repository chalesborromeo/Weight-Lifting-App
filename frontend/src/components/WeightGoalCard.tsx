import { useState } from "react";
import { Target, Pencil } from "lucide-react";
import { profileApi } from "@/api";
import type { BodyMetric, Profile } from "@/types";

type Props = {
  profile: Profile | null;
  metrics: BodyMetric[];
  onProfileUpdate: (p: Profile) => void;
};

/**
 * Goal tracking: shows progress bar from baseline (oldest measurement) toward the goal.
 * Falls back to an inline form when no goal is set.
 */
export function WeightGoalCard({ profile, metrics, onProfileUpdate }: Props) {
  const [editing, setEditing] = useState(false);
  const goal = profile?.goal_weight ?? null;

  if (goal == null || editing) {
    return <GoalForm profile={profile} onSaved={onProfileUpdate} onCancel={() => setEditing(false)} />;
  }

  const latest = metrics[0]; // newest first from API
  const baseline = metrics[metrics.length - 1]; // oldest entry as starting point

  if (!latest) {
    return (
      <GoalDisplay
        goal={goal}
        helper="Log your first weight to start tracking progress."
        onEdit={() => setEditing(true)}
      />
    );
  }

  const current = latest.weight;
  const toGo = +(current - goal).toFixed(1); // positive = cutting, negative = bulking
  const direction: "cut" | "bulk" | "achieved" =
    Math.abs(toGo) < 0.05 ? "achieved" : toGo > 0 ? "cut" : "bulk";

  // Progress from baseline toward goal (clamped 0..1)
  let progress: number | null = null;
  if (baseline && baseline.id !== latest.id) {
    const start = baseline.weight;
    const totalNeeded = start - goal; // cut: +; bulk: -
    const done = start - current;
    if (Math.abs(totalNeeded) > 0.01) {
      progress = Math.max(0, Math.min(1, done / totalNeeded));
    }
  }

  return (
    <div className="bg-card rounded-[20px] p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs uppercase tracking-wide text-muted-foreground">
          <Target className="w-3.5 h-3.5" />
          Goal
        </div>
        <button
          onClick={() => setEditing(true)}
          className="text-muted-foreground hover:text-foreground p-1"
          aria-label="Edit goal"
        >
          <Pencil className="w-3.5 h-3.5" />
        </button>
      </div>

      <div className="flex items-baseline justify-between">
        <div>
          <div className="text-2xl font-semibold text-foreground">
            {goal}
            <span className="ml-1 text-sm font-normal text-muted-foreground">lbs goal</span>
          </div>
          <div className="text-xs text-muted-foreground mt-1">
            currently {current} lbs ·{" "}
            {direction === "achieved"
              ? "goal reached 🎉"
              : direction === "cut"
              ? `${toGo} lbs to lose`
              : `${Math.abs(toGo)} lbs to gain`}
          </div>
        </div>
      </div>

      {progress !== null && (
        <div className="space-y-1">
          <div className="h-2 bg-background rounded-full overflow-hidden">
            <div
              className="h-full bg-accent rounded-full transition-all"
              style={{ width: `${Math.round(progress * 100)}%` }}
            />
          </div>
          <div className="text-xs text-muted-foreground text-right">
            {Math.round(progress * 100)}% of the way there
          </div>
        </div>
      )}
    </div>
  );
}

function GoalDisplay({
  goal,
  helper,
  onEdit,
}: {
  goal: number;
  helper: string;
  onEdit: () => void;
}) {
  return (
    <div className="bg-card rounded-[20px] p-4 flex items-center justify-between">
      <div>
        <div className="flex items-center gap-2 text-xs uppercase tracking-wide text-muted-foreground">
          <Target className="w-3.5 h-3.5" />
          Goal
        </div>
        <div className="text-2xl font-semibold text-foreground mt-1">
          {goal}
          <span className="ml-1 text-sm font-normal text-muted-foreground">lbs</span>
        </div>
        <div className="text-xs text-muted-foreground mt-1">{helper}</div>
      </div>
      <button
        onClick={onEdit}
        className="text-muted-foreground hover:text-foreground p-2"
        aria-label="Edit goal"
      >
        <Pencil className="w-4 h-4" />
      </button>
    </div>
  );
}

function GoalForm({
  profile,
  onSaved,
  onCancel,
}: {
  profile: Profile | null;
  onSaved: (p: Profile) => void;
  onCancel: () => void;
}) {
  const [value, setValue] = useState<string>(profile?.goal_weight?.toString() ?? "");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const hasProfile = profile !== null;
  const canSubmit = value.trim().length > 0 && !submitting && hasProfile;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;
    setSubmitting(true);
    setError(null);
    try {
      const updated = await profileApi.update({ goal_weight: Number(value) });
      onSaved(updated);
      onCancel();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSubmitting(false);
    }
  };

  const handleClear = async () => {
    setSubmitting(true);
    setError(null);
    try {
      const updated = await profileApi.update({ goal_weight: null });
      onSaved(updated);
      onCancel();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to clear goal");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-card rounded-[20px] p-4 space-y-3">
      <div className="flex items-center gap-2 text-xs uppercase tracking-wide text-muted-foreground">
        <Target className="w-3.5 h-3.5" />
        {profile?.goal_weight != null ? "Edit goal" : "Set a weight goal"}
      </div>

      {!hasProfile && (
        <p className="text-xs text-muted-foreground">
          You need a profile first — visit Edit Profile to create one.
        </p>
      )}

      <label className="flex items-center justify-between px-2">
        <span className="text-sm text-foreground">Goal weight (lbs)</span>
        <input
          type="number"
          step="any"
          min="0"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="e.g. 180"
          autoFocus
          className="w-28 px-3 py-2 bg-background rounded-[10px] text-foreground text-right outline-none focus:ring-2 focus:ring-accent/30"
        />
      </label>

      {error && <div className="text-sm text-destructive">{error}</div>}

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={!canSubmit}
          className={`flex-1 px-4 py-2.5 rounded-[12px] transition-all ${
            canSubmit
              ? "bg-accent text-white active:scale-95"
              : "bg-inactive text-muted-foreground cursor-not-allowed"
          }`}
        >
          {submitting ? "Saving..." : "Save"}
        </button>
        {profile?.goal_weight != null && (
          <button
            type="button"
            onClick={handleClear}
            disabled={submitting}
            className="px-4 py-2.5 rounded-[12px] text-sm text-destructive hover:bg-destructive/10 transition-colors"
          >
            Clear
          </button>
        )}
        <button
          type="button"
          onClick={onCancel}
          disabled={submitting}
          className="px-4 py-2.5 rounded-[12px] text-sm text-muted-foreground hover:text-foreground"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
