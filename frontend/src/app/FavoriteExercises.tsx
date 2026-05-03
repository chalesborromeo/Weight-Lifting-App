import { useEffect, useState } from "react";
import { Plus, Star, Trash2 } from "lucide-react";
import { favoriteExercisesApi, exercisesApi } from "@/api";
import { SectionHeader } from "@/components/SectionHeader";
import type { FavoriteExercise, ExerciseCatalogEntry } from "@/types";

const DATALIST_ID = "fav-exercise-catalog";

export default function FavoriteExercises() {
  const [favorites, setFavorites] = useState<FavoriteExercise[]>([]);
  const [catalog, setCatalog] = useState<ExerciseCatalogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const [favs, cat] = await Promise.all([
        favoriteExercisesApi.list(),
        exercisesApi.catalog().catch(() => [] as ExerciseCatalogEntry[]),
      ]);
      setFavorites(favs);
      setCatalog(cat);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load favorites");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const handleAdded = (fav: FavoriteExercise) => {
    setFavorites((prev) => [...prev, fav]);
    setShowForm(false);
  };

  const handleRemove = async (id: number) => {
    const previous = favorites;
    setFavorites((prev) => prev.filter((f) => f.id !== id));
    try {
      await favoriteExercisesApi.remove(id);
    } catch {
      setFavorites(previous);
    }
  };

  // Group favorites by catalog muscle group, falling back to "Other"
  const groupMap = Object.fromEntries(catalog.map((e) => [e.name, e.group]));
  const grouped = favorites.reduce<Record<string, FavoriteExercise[]>>((acc, fav) => {
    const group = groupMap[fav.name] ?? "Other";
    (acc[group] ??= []).push(fav);
    return acc;
  }, {});
  const groupOrder = ["Chest", "Back", "Legs", "Shoulders", "Arms", "Core", "Cardio", "Other"];
  const sortedGroups = groupOrder.filter((g) => grouped[g]);

  return (
    <div className="space-y-6">
      <SectionHeader title="Favorite Exercises" />

      <datalist id={DATALIST_ID}>
        {catalog.map((ex) => (
          <option key={ex.name} value={ex.name} label={ex.group} />
        ))}
      </datalist>

      <button
        onClick={() => setShowForm((v) => !v)}
        className="w-full flex items-center justify-center gap-2 bg-accent text-white px-4 py-3 rounded-[15px] active:scale-95 transition-transform"
      >
        <Plus className="w-4 h-4" />
        {showForm ? "Cancel" : "Add Favorite"}
      </button>

      {showForm && <AddForm onAdded={handleAdded} favoritedNames={favorites.map((f) => f.name)} />}

      {loading && <div className="text-sm text-muted-foreground">Loading...</div>}
      {error && <div className="text-sm text-destructive">{error}</div>}

      {!loading && favorites.length === 0 && !showForm && (
        <div className="bg-card rounded-[20px] p-8 text-center text-sm text-muted-foreground">
          No favorites yet. Add exercises you do regularly.
        </div>
      )}

      {sortedGroups.map((group) => (
        <div key={group} className="space-y-2">
          <h2 className="text-xs uppercase tracking-wide text-muted-foreground px-1">{group}</h2>
          {grouped[group].map((fav) => (
            <FavCard key={fav.id} fav={fav} onRemove={() => handleRemove(fav.id)} />
          ))}
        </div>
      ))}
    </div>
  );
}

function FavCard({ fav, onRemove }: { fav: FavoriteExercise; onRemove: () => void }) {
  return (
    <div className="bg-card rounded-[20px] px-4 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <Star className="w-4 h-4 text-accent fill-accent shrink-0" />
        <span className="text-sm font-medium text-foreground">{fav.name}</span>
      </div>
      <button
        onClick={onRemove}
        className="text-muted-foreground hover:text-destructive transition-colors p-2"
        aria-label="Remove favorite"
      >
        <Trash2 className="w-4 h-4" />
      </button>
    </div>
  );
}

function AddForm({
  onAdded,
  favoritedNames,
}: {
  onAdded: (fav: FavoriteExercise) => void;
  favoritedNames: string[];
}) {
  const [name, setName] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const alreadyFavorited = favoritedNames.includes(name.trim());
  const canSubmit = name.trim().length > 0 && !submitting && !alreadyFavorited;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;
    setSubmitting(true);
    setError(null);
    try {
      const created = await favoriteExercisesApi.add(name.trim());
      setName("");
      onAdded(created);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add favorite");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-card rounded-[20px] p-4 space-y-3">
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Exercise name"
        list={DATALIST_ID}
        autoFocus
        className="w-full px-4 py-3 bg-background rounded-[12px] text-foreground placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-accent/30"
      />
      {alreadyFavorited && (
        <p className="text-xs text-muted-foreground px-1">Already in your favorites.</p>
      )}
      {error && <div className="text-sm text-destructive">{error}</div>}
      <button
        type="submit"
        disabled={!canSubmit}
        className={`w-full px-4 py-3 rounded-[12px] transition-all ${
          canSubmit
            ? "bg-accent text-white active:scale-95"
            : "bg-inactive text-muted-foreground cursor-not-allowed"
        }`}
      >
        {submitting ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
