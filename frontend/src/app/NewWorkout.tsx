import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router";
import { ApiError, workoutsApi, exercisesApi, favoriteExercisesApi } from "@/api";
import type { ExerciseCreate, ExerciseCatalogEntry, SetCreate, FavoriteExercise } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";
import { SectionHeader } from "@/components/SectionHeader";

const EXERCISE_DATALIST_ID = "workout-exercise-catalog";

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
  const [isPublic, setIsPublic] = useState(true);
  const [exercises, setExercises] = useState<DraftExercise[]>([emptyExercise()]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [workoutTypes, setWorkoutTypes] = useState<string[]>([]);
  const [catalog, setCatalog] = useState<ExerciseCatalogEntry[]>([]);
  const [favorites,setFavorites]=useState<FavoriteExercise[]>([]);

  useEffect(() => {
    exercisesApi.workoutTypes().then(setWorkoutTypes).catch(() => setWorkoutTypes([]));
    exercisesApi.catalog().then(setCatalog).catch(() => setCatalog([]));
    favoriteExercisesApi.list().then(setFavorites).catch(()=>setFavorites([]));
  }, []);

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

  function isFavorited(name:string){
    return favorites.some((f)=>f.name.toLowerCase()===name.toLowerCase());
  }

  async function toggleFavorite(name: string){
    if(!name.trim()) return;
    const existing=favorites.find((f)=>f.name.toLowerCase()===name.toLowerCase());
    if(existing){
      await favoriteExercisesApi.remove(existing.id);
      setFavorites((prev)=>prev.filter((f)=>f.id!==existing.id));
    }else{
      const added=await favoriteExercisesApi.add(name);
      setFavorites((prev)=>[...prev,added]);
    }
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
        is_public: isPublic,
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
        <SectionHeader title="New Workout" />
        <p className="text-sm text-muted-foreground">
          You need a current user first.{" "}
          <Link to="/users" className="text-accent underline">Go pick one.</Link>
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-6">
      <SectionHeader title="New Workout" />

      {/* Shared exercise-name autocomplete (browser-native, allows custom entries) */}
      <datalist id={EXERCISE_DATALIST_ID}>
        {catalog.map((ex) => (
          <option key={ex.name} value={ex.name} label={ex.group} />
        ))}
      </datalist>

      <div className="bg-card rounded-[20px] p-6 space-y-3">
        <input
          required
          placeholder="Name (e.g. Push Day)"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full px-4 py-3 bg-background rounded-[15px] text-sm text-foreground placeholder:text-muted-foreground outline-none focus:ring-1 focus:ring-accent"
        />
        <select
          required
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="w-full px-4 py-3 bg-background rounded-[15px] text-sm text-foreground outline-none focus:ring-1 focus:ring-accent appearance-none cursor-pointer"
        >
          <option value="" disabled>
            Select workout type...
          </option>
          {workoutTypes.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
        <label className="block text-xs text-muted-foreground">
          Duration (minutes)
          <input
            type="number"
            min={0}
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
            className="w-full mt-1 px-4 py-3 bg-background rounded-[15px] text-sm text-foreground outline-none focus:ring-1 focus:ring-accent"
          />
        </label>
        <button
          type="button"
          onClick={() => setIsPublic((v) => !v)}
          className={`w-full flex items-center justify-between px-4 py-3 rounded-[15px] text-sm transition-colors ${
            isPublic ? "bg-background text-foreground" : "bg-background text-muted-foreground"
          }`}
        >
          <span>{isPublic ? "🌐 Public — visible to peers" : "🔒 Private — only you can see this"}</span>
          <span className={`w-10 h-6 rounded-full transition-colors flex items-center px-0.5 ${isPublic ? "bg-accent" : "bg-inactive"}`}>
            <span className={`w-5 h-5 rounded-full bg-white shadow transition-transform ${isPublic ? "translate-x-4" : "translate-x-0"}`} />
          </span>
        </button>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm uppercase tracking-wide text-muted-foreground">Exercises</h2>
          <button
            type="button"
            onClick={() => setExercises((p) => [...p, emptyExercise()])}
            className="text-xs px-3 py-1.5 border border-inactive text-muted-foreground rounded-[15px] hover:border-foreground hover:text-foreground transition-colors"
          >
            + Exercise
          </button>
        </div>

        {exercises.map((ex, i) => (
          <div key={i} className="bg-card rounded-[20px] p-4 space-y-3">
            <div className="flex gap-2">
              <input
                required
                placeholder="Exercise name"
                value={ex.name}
                onChange={(e) => updateExercise(i, { name: e.target.value })}
                list={EXERCISE_DATALIST_ID}
                className="flex-1 px-4 py-3 bg-background rounded-[15px] text-sm text-foreground placeholder:text-muted-foreground outline-none focus:ring-1 focus:ring-accent"
              />
              <button
                type="button"
                onClick={()=>toggleFavorite(ex.name)}
                disabled={!ex.name.trim()}
                title={isFavorited(ex.name)? "Remove from favorites":"Add to favorites"}
                className="text-lg px-2 text-yellow-400 disabled:opacity-30 hover:scale-110 transition-transform"
                >
                  {isFavorited(ex.name)?"★":"☆"}
              </button>
              {exercises.length > 1 && (
                <button
                  type="button"
                  onClick={() => setExercises((p) => p.filter((_, idx) => idx !== i))}
                  className="text-xs px-3 py-1.5 text-destructive border border-destructive/20 rounded-[15px] hover:bg-destructive/10 transition-colors"
                >
                  Remove
                </button>
              )}
            </div>

            <div className="space-y-2">
              {ex.sets.map((s, j) => (
                <div key={j} className="flex gap-2 items-center text-sm">
                  <span className="text-xs text-muted-foreground w-8">#{j + 1}</span>
                  <input
                    type="number"
                    placeholder="weight"
                    value={s.weight}
                    onChange={(e) => updateSet(i, j, { weight: Number(e.target.value) })}
                    className="w-24 px-3 py-2 bg-background rounded-[10px] text-foreground outline-none focus:ring-1 focus:ring-accent"
                  />
                  <input
                    type="number"
                    placeholder="reps"
                    value={s.reps}
                    onChange={(e) => updateSet(i, j, { reps: Number(e.target.value) })}
                    className="w-24 px-3 py-2 bg-background rounded-[10px] text-foreground outline-none focus:ring-1 focus:ring-accent"
                  />
                  {ex.sets.length > 1 && (
                    <button
                      type="button"
                      onClick={() =>
                        updateExercise(i, { sets: ex.sets.filter((_, k) => k !== j) })
                      }
                      className="text-xs px-2 py-1 text-destructive hover:bg-destructive/10 rounded-[10px] transition-colors"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={() => updateExercise(i, { sets: [...ex.sets, emptySet()] })}
                className="text-xs px-3 py-1.5 border border-inactive text-muted-foreground rounded-[15px] hover:border-foreground hover:text-foreground transition-colors"
              >
                + Set
              </button>
            </div>
          </div>
        ))}
      </div>

      {error && <div className="text-sm text-destructive">{error}</div>}

      <button
        type="submit"
        disabled={submitting}
        className="w-full px-5 py-4 bg-accent text-white rounded-[15px] disabled:opacity-50 hover:bg-accent/90 transition-colors"
      >
        {submitting ? "Saving..." : "Create workout"}
      </button>
    </form>
  );
}
