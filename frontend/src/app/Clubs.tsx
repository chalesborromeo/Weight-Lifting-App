import { useEffect, useState } from "react";
import { clubsApi } from "@/api";
import type { Club } from "@/types";

export default function Clubs() {
  const [clubs, setClubs] = useState<Club[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        setClubs(await clubsApi.list());
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load clubs");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl tracking-tight">Clubs</h1>

      {loading && <div className="text-sm text-black/60">Loading…</div>}
      {error && <div className="text-sm text-red-600">{error}</div>}
      {!loading && clubs.length === 0 && (
        <div className="text-sm text-black/60">No clubs yet.</div>
      )}

      <ul className="space-y-3">
        {clubs.map((c) => (
          <li key={c.id} className="border border-black/10 rounded-lg p-4">
            <div className="flex items-baseline justify-between">
              <div className="text-base">{c.name}</div>
              <div className="text-xs text-black/50">{c.privacy}</div>
            </div>
            <div className="text-xs text-black/60 mt-1">
              owner: {c.owner.email} · {c.members.length} member(s)
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
