import { useEffect, useState } from "react";
import { Link } from "react-router";
import { clubsApi } from "@/api";
import type { Club } from "@/types";
import { SectionHeader } from "@/components/SectionHeader";

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
      <SectionHeader
        title="Clubs"
        action={
          <Link
            to="/clubs/new"
            className="px-4 py-2 text-sm bg-accent text-white rounded-[15px] hover:bg-accent/90 transition-colors"
          >
            + Create Club
          </Link>
        }
      />

      {loading && <div className="text-sm text-muted-foreground">Loading...</div>}
      {error && <div className="text-sm text-destructive">{error}</div>}
      {!loading && clubs.length === 0 && (
        <div className="bg-card rounded-[20px] p-12 text-center space-y-3">
          <p className="text-foreground font-medium">No clubs yet</p>
          <p className="text-sm text-muted-foreground">
            <Link to="/clubs/new" className="text-accent hover:underline">Create the first one</Link>
          </p>
        </div>
      )}

      <div className="space-y-3">
        {clubs.map((c) => (
          <Link
            key={c.id}
            to={`/clubs/${c.id}`}
            className="block bg-card rounded-[20px] p-5 hover:bg-card/80 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-semibold text-foreground">{c.name}</h3>
                  <span className="text-[11px] bg-accent/10 text-accent px-2 py-0.5 rounded-full uppercase tracking-wide">
                    {c.privacy}
                  </span>
                </div>
                {c.description && (
                  <p className="text-sm text-muted-foreground line-clamp-2">{c.description}</p>
                )}
                <div className="text-xs text-muted-foreground">
                  by {c.owner.email}
                </div>
              </div>

              <div className="flex flex-col items-end gap-2">
                {/* Stacked avatars */}
                <div className="flex -space-x-2">
                  {c.members.slice(0, 4).map((m) => (
                    <div
                      key={m.id}
                      className="w-8 h-8 rounded-full bg-accent text-white flex items-center justify-center text-[10px] font-bold border-2 border-card"
                    >
                      {m.email.charAt(0).toUpperCase()}
                    </div>
                  ))}
                  {c.members.length > 4 && (
                    <div className="w-8 h-8 rounded-full bg-inactive text-foreground flex items-center justify-center text-[10px] font-bold border-2 border-card">
                      +{c.members.length - 4}
                    </div>
                  )}
                </div>
                <span className="text-xs text-muted-foreground">
                  {c.members.length} member{c.members.length !== 1 ? "s" : ""}
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
