import { useState } from "react";
import { useNavigate, Link } from "react-router";
import { ApiError, workoutsApi } from "@/api";
import type { ExerciseCreate, SetCreate } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";

type DraftSet = SetCreate;
type DraftExercise = { name: string; sets: DraftSet[] };

const emptySet = (): DraftSet => ({ weight: 0, reps: 0 });
const emptyExercise = (): DraftExercise => ({ name: "", sets: [emptySet()] });

export default function NewWorkout() {
  const { userId } = useCurrentUser();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [type, setType] = useState("");
  const [duration, setDuration] = useState(30);
  const [exercises, setExercises] = useState<DraftExercise[]>([emptyExercise()]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function updateExercise(i: number, patch: Partial<DraftExercise>) {
    setExercises((prev) => prev.map((ex, idx) => (idx === i ? { ...ex, ...patch } : ex)));
  }

  function updateSet(exIdx: number, setIdx: number, patch: Partial<DraftSet>) {
    setExercises((prev) =>
      prev.map((ex, i) =>
        i === exIdx
          ? { ...ex, sets: ex.sets.map((s, j) => (j === setIdx ? { ...s, ...patch } : s)) }
          : ex,
      ),
    );
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (userId === null) {
      setError("Pick a current user first.");
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const payload = {
        user_id: userId,
        name,
        type,
        duration,
        exercises: exercises as ExerciseCreate[],
      };
      await workoutsApi.create(payload);
      navigate("/workouts");
    } catch (err) {
      if (err instanceof ApiError) setError(`${err.status}: ${JSON.stringify(err.body)}`);
      else setError(err instanceof Error ? err.message : "Failed to create workout");
    } finally {
      setSubmitting(false);
    }
  }

  if (userId === null) {
    return (
      <div className="space-y-3">
        <h1 className="text-2xl tracking-tight">New Workout</h1>
        <p className="text-sm text-black/60">
          You need a current user first.{" "}
          <Link to="/users" className="underline">Go pick one.</Link>
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-6">
      <h1 className="text-2xl tracking-tight">New Workout</h1>

      <div className="space-y-3">
        <input
          required
          placeholder="Name (e.g. Push Day)"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full px-3 py-2 border border-black/20 rounded-md text-sm"
        />
        <input
          required
          placeholder="Type (e.g. Strength)"
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="w-full px-3 py-2 border border-black/20 rounded-md text-sm"
        />
        <label className="block text-xs text-black/60">
          Duration (minutes)
          <input
            type="number"
            min={0}
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
            className="w-full mt-1 px-3 py-2 border border-black/20 rounded-md text-sm"
          />
        </label>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm uppercase tracking-wide text-black/60">Exercises</h2>
          <button
            type="button"
            onClick={() => setExercises((p) => [...p, emptyExercise()])}
            className="text-xs px-2 py-1 border border-black/20 rounded-md"
          >
            + Exercise
          </button>
        </div>

        {exercises.map((ex, i) => (
          <div key={i} className="border border-black/10 rounded-lg p-3 space-y-3">
            <div className="flex gap-2">
              <input
                required
                placeholder="Exercise name"
                value={ex.name}
                onChange={(e) => updateExercise(i, { name: e.target.value })}
                className="flex-1 px-3 py-2 border border-black/20 rounded-md text-sm"
              />
              {exercises.length > 1 && (
                <button
                  type="button"
                  onClick={() => setExercises((p) => p.filter((_, idx) => idx !== i))}
                  className="text-xs px-2 py-1 border border-black/20 rounded-md"
                >
                  Remove
                </button>
              )}
            </div>

            <div className="space-y-2">
              {ex.sets.map((s, j) => (
                <div key={j} className="flex gap-2 items-center text-sm">
                  <span className="text-xs text-black/50 w-8">#{j + 1}</span>
                  <input
                    type="number"
                    placeholder="weight"
                    value={s.weight}
                    onChange={(e) => updateSet(i, j, { weight: Number(e.target.value) })}
                    className="w-24 px-2 py-1 border border-black/20 rounded-md"
                  />
                  <input
                    type="number"
                    placeholder="reps"
                    value={s.reps}
                    onChange={(e) => updateSet(i, j, { reps: Number(e.target.value) })}
                    className="w-24 px-2 py-1 border border-black/20 rounded-md"
                  />
                  {ex.sets.length > 1 && (
                    <button
                      type="button"
                      onClick={() =>
                        updateExercise(i, { sets: ex.sets.filter((_, k) => k !== j) })
                      }
                      className="text-xs px-2 py-1 border border-black/20 rounded-md"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={() => updateExercise(i, { sets: [...ex.sets, emptySet()] })}
                className="text-xs px-2 py-1 border border-black/20 rounded-md"
              >
                + Set
              </button>
            </div>
          </div>
        ))}
      </div>

      {error && <div className="text-sm text-red-600">{error}</div>}

      <button
        type="submit"
        disabled={submitting}
        className="px-5 py-2 bg-black text-white text-sm rounded-md disabled:opacity-50"
      >
        {submitting ? "Saving…" : "Create workout"}
      </button>
    </form>
  );
}
