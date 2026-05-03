import { useEffect, useState } from "react";
import { Dumbbell, RefreshCw, Clock, ChevronDown, ChevronUp } from "lucide-react";
import { suggestionsApi } from "@/api/suggestions";
import { SectionHeader } from "@/components/SectionHeader";
import type { WorkoutSuggestion, ExerciseSuggestion } from "@/types";

function ExerciseCard({ ex }: { ex: ExerciseSuggestion }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="bg-background rounded-[16px] overflow-hidden">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center gap-3 px-4 py-3 text-left"
      >
        <div className="flex-1 min-w-0">
          <div className="text-sm font-semibold text-foreground truncate">{ex.exercise_name}</div>
          <div className="text-xs text-muted-foreground mt-0.5">
            {ex.suggested_sets} sets × {ex.suggested_reps} reps
            {ex.suggested_weight != null && ` @ ${ex.suggested_weight} lbs`}
          </div>
        </div>
        {open ? (
          <ChevronUp className="w-4 h-4 text-muted-foreground shrink-0" />
        ) : (
          <ChevronDown className="w-4 h-4 text-muted-foreground shrink-0" />
        )}
      </button>
      {open && (
        <div className="px-4 pb-3 space-y-2 border-t border-border pt-3">
          <p className="text-xs text-muted-foreground leading-relaxed">{ex.rationale}</p>
          {(ex.previous_best_weight != null || ex.previous_best_reps != null) && (
            <div className="flex gap-3 text-xs">
              {ex.previous_best_weight != null && (
                <span className="text-muted-foreground">
                  Previous best: <span className="text-foreground font-medium">{ex.previous_best_weight} lbs</span>
                </span>
              )}
              {ex.previous_best_reps != null && (
                <span className="text-muted-foreground">
                  × <span className="text-foreground font-medium">{ex.previous_best_reps} reps</span>
                </span>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function SuggestedWorkout() {
  const [suggestion, setSuggestion] = useState<WorkoutSuggestion | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await suggestionsApi.nextWorkout();
      setSuggestion(data);
    } catch {
      setError("Add favorite exercises first — star an exercise while logging a workout, then come back here.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <SectionHeader title="Suggested Workout" />
        <button
          onClick={load}
          disabled={loading}
          className="flex items-center gap-1.5 text-xs text-accent disabled:opacity-40 transition-opacity"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          Regenerate
        </button>
      </div>

      {loading && (
        <div className="bg-card rounded-[20px] p-12 text-center">
          <p className="text-sm text-muted-foreground">Generating your personalized workout...</p>
        </div>
      )}

      {error && (
        <div className="bg-card rounded-[20px] p-8 text-center space-y-3">
          <Dumbbell className="w-10 h-10 text-muted-foreground mx-auto" />
          <p className="text-sm text-muted-foreground">{error}</p>
        </div>
      )}

      {!loading && suggestion && (
        <>
          {/* Header card */}
          <div className="bg-card rounded-[20px] p-5 space-y-3">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="text-lg font-semibold text-foreground">{suggestion.workout_name}</h2>
                <span className="text-xs text-accent bg-accent/10 px-2.5 py-1 rounded-full uppercase tracking-wide inline-block mt-1">
                  {suggestion.workout_type}
                </span>
              </div>
              <div className="flex items-center gap-1.5 text-sm text-muted-foreground shrink-0">
                <Clock className="w-4 h-4" />
                {Math.round(suggestion.estimated_duration)} min
              </div>
            </div>
            <div className="grid grid-cols-2 gap-2 pt-1 border-t border-border">
              <div className="text-center py-2">
                <div className="text-xl font-bold text-foreground">{suggestion.total_exercises}</div>
                <div className="text-[11px] text-muted-foreground uppercase tracking-wide">Exercises</div>
              </div>
              <div className="text-center py-2">
                <div className="text-xl font-bold text-foreground">
                  {suggestion.exercises.reduce((s, e) => s + e.suggested_sets, 0)}
                </div>
                <div className="text-[11px] text-muted-foreground uppercase tracking-wide">Total Sets</div>
              </div>
            </div>
          </div>

          {/* Exercise list */}
          <div className="bg-card rounded-[20px] p-4 space-y-2">
            <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide px-1 pb-1">
              Exercises
            </h3>
            {suggestion.exercises.map((ex) => (
              <ExerciseCard key={ex.exercise_name} ex={ex} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
