import { useEffect, useState } from "react";
import { Plus, Trash2, Trophy } from "lucide-react";
import { prsApi, exercisesApi } from "@/api";
import { useCurrentUser } from "@/context/CurrentUser";
import { SectionHeader } from "@/components/SectionHeader";
import type { PR, PRCreate, ExerciseCatalogEntry } from "@/types";

type Tab = "mine" | "leaderboard";
const EXERCISE_DATALIST_ID = "exercise-catalog";

export default function PRs() {
  const { user } = useCurrentUser();
  const [tab, setTab] = useState<Tab>("mine");
  const [catalog, setCatalog] = useState<ExerciseCatalogEntry[]>([]);

  useEffect(() => {
    exercisesApi.catalog().then(setCatalog).catch(() => setCatalog([]));
  }, []);

  return (
    <div className="space-y-6">
      <SectionHeader title="PRs" />

      <div className="flex gap-1 bg-card rounded-[15px] p-1">
        <TabButton active={tab === "mine"} onClick={() => setTab("mine")}>
          My PRs
        </TabButton>
        <TabButton active={tab === "leaderboard"} onClick={() => setTab("leaderboard")}>
          Leaderboard
        </TabButton>
      </div>

      {/* Single shared datalist for any exercise input on this page */}
      <datalist id={EXERCISE_DATALIST_ID}>
        {catalog.map((ex) => (
          <option key={ex.name} value={ex.name} label={ex.group} />
        ))}
      </datalist>

      {tab === "mine" ? <MyPRs /> : <Leaderboard currentUserId={user?.id} />}
    </div>
  );
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex-1 px-4 py-2 text-sm rounded-[12px] transition-colors ${
        active ? "bg-accent text-white" : "text-muted-foreground hover:text-foreground"
      }`}
    >
      {children}
    </button>
  );
}

// ----- My PRs -----

function MyPRs() {
  const [prs, setPrs] = useState<PR[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      setPrs(await prsApi.list());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load PRs");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const handleCreated = (newPR: PR) => {
    setPrs((prev) => [newPR, ...prev]);
    setShowForm(false);
  };

  const handleDelete = async (id: number) => {
    const previous = prs;
    setPrs(prev => prev.filter(p => p.id !== id));
    try {
      await prsApi.remove(id);
    } catch (err) {
      // restore on failure
      setPrs(previous);
      setError(err instanceof Error ? err.message : "Failed to delete");
    }
  };

  return (
    <div className="space-y-3">
      <button
        onClick={() => setShowForm((v) => !v)}
        className="w-full flex items-center justify-center gap-2 bg-accent text-white px-4 py-3 rounded-[15px] active:scale-95 transition-transform"
      >
        <Plus className="w-4 h-4" />
        {showForm ? "Cancel" : "Log a PR"}
      </button>

      {showForm && <AddPRForm onCreated={handleCreated} />}

      {loading && <div className="text-sm text-muted-foreground">Loading...</div>}
      {error && <div className="text-sm text-destructive">{error}</div>}
      {!loading && prs.length === 0 && (
        <div className="bg-card rounded-[20px] p-8 text-center text-sm text-muted-foreground">
          No PRs yet. Log your first one above.
        </div>
      )}

      {prs.map((pr) => (
        <PRCard key={pr.id} pr={pr} onDelete={() => handleDelete(pr.id)} />
      ))}
    </div>
  );
}

function AddPRForm({ onCreated }: { onCreated: (pr: PR) => void }) {
  const [exercise, setExercise] = useState("");
  const [weight, setWeight] = useState("");
  const [reps, setReps] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = exercise.trim() && weight && reps && !submitting;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;
    setSubmitting(true);
    setError(null);
    try {
      const body: PRCreate = {
        exercise_name: exercise.trim(),
        weight: Number(weight),
        reps: Number(reps),
      };
      const created = await prsApi.create(body);
      setExercise("");
      setWeight("");
      setReps("");
      onCreated(created);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to log PR");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-card rounded-[20px] p-4 space-y-3">
      <input
        value={exercise}
        onChange={(e) => setExercise(e.target.value)}
        placeholder="Exercise (e.g. Bench Press)"
        list={EXERCISE_DATALIST_ID}
        className="w-full px-4 py-3 bg-background rounded-[12px] text-foreground placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-accent/30"
        autoFocus
      />
      <div className="flex gap-3">
        <input
          type="number"
          inputMode="decimal"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
          placeholder="Weight (lbs)"
          className="flex-1 px-4 py-3 bg-background rounded-[12px] text-foreground placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-accent/30"
        />
        <input
          type="number"
          inputMode="numeric"
          value={reps}
          onChange={(e) => setReps(e.target.value)}
          placeholder="Reps"
          className="w-28 px-4 py-3 bg-background rounded-[12px] text-foreground placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-accent/30"
        />
      </div>
      {error && <div className="text-sm text-destructive">{error}</div>}
      <button
        type="submit"
        disabled={!canSubmit}
        className={`w-full px-4 py-3 rounded-[12px] transition-all ${
          canSubmit ? "bg-accent text-white active:scale-95" : "bg-inactive text-muted-foreground cursor-not-allowed"
        }`}
      >
        {submitting ? "Saving..." : "Save PR"}
      </button>
    </form>
  );
}

function PRCard({ pr, onDelete }: { pr: PR; onDelete: () => void }) {
  return (
    <div className="bg-card rounded-[20px] p-4 flex items-center justify-between">
      <div>
        <div className="text-base font-semibold text-foreground">{pr.exercise_name}</div>
        <div className="text-sm text-muted-foreground mt-1">
          {pr.weight} lbs × {pr.reps} · {new Date(pr.date).toLocaleDateString()}
        </div>
      </div>
      <button
        onClick={onDelete}
        className="text-muted-foreground hover:text-destructive transition-colors p-2"
        aria-label="Delete PR"
      >
        <Trash2 className="w-4 h-4" />
      </button>
    </div>
  );
}

// ----- Leaderboard -----

function Leaderboard({ currentUserId }: { currentUserId: number | undefined }) {
  const [exercise, setExercise] = useState("");
  const [results, setResults] = useState<PR[]>([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!exercise.trim()) return;
    setLoading(true);
    setError(null);
    setSearched(true);
    try {
      setResults(await prsApi.leaderboard(exercise.trim()));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load leaderboard");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-3">
      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          value={exercise}
          onChange={(e) => setExercise(e.target.value)}
          placeholder="Exercise name"
          list={EXERCISE_DATALIST_ID}
          className="flex-1 px-4 py-3 bg-card rounded-[15px] text-foreground placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-accent/30"
        />
        <button
          type="submit"
          disabled={!exercise.trim() || loading}
          className={`px-5 py-3 rounded-[15px] ${
            exercise.trim() && !loading ? "bg-accent text-white active:scale-95" : "bg-inactive text-muted-foreground"
          }`}
        >
          Search
        </button>
      </form>

      {loading && <div className="text-sm text-muted-foreground">Loading...</div>}
      {error && <div className="text-sm text-destructive">{error}</div>}

      {searched && !loading && results.length === 0 && (
        <div className="bg-card rounded-[20px] p-8 text-center text-sm text-muted-foreground">
          No PRs logged for "{exercise}" yet.
        </div>
      )}

      {results.map((pr, i) => (
        <LeaderboardRow key={pr.id} rank={i + 1} pr={pr} isMe={pr.user_id === currentUserId} />
      ))}
    </div>
  );
}

function LeaderboardRow({ rank, pr, isMe }: { rank: number; pr: PR; isMe: boolean }) {
  const medal = rank === 1 ? "text-amber-400" : rank === 2 ? "text-zinc-400" : rank === 3 ? "text-orange-400" : "text-muted-foreground";
  return (
    <div className={`bg-card rounded-[20px] p-4 flex items-center gap-4 ${isMe ? "ring-2 ring-accent" : ""}`}>
      <div className={`w-8 flex items-center justify-center ${medal}`}>
        {rank <= 3 ? <Trophy className="w-5 h-5" /> : <span className="text-sm">#{rank}</span>}
      </div>
      <div className="flex-1">
        <div className="text-base font-semibold text-foreground">{pr.user.email}{isMe && <span className="text-xs text-accent ml-2">(you)</span>}</div>
        <div className="text-xs text-muted-foreground mt-0.5">
          {new Date(pr.date).toLocaleDateString()}
        </div>
      </div>
      <div className="text-right">
        <div className="text-lg font-semibold text-foreground">{pr.weight} <span className="text-xs text-muted-foreground">lbs</span></div>
        <div className="text-xs text-muted-foreground">× {pr.reps}</div>
      </div>
    </div>
  );
}
