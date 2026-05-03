import { useEffect, useState } from "react";
import { Link } from "react-router";
import { usersApi } from "@/api/users";
import { peersApi } from "@/api/peers";
import { useCurrentUser } from "@/context/CurrentUser";
import { SectionHeader } from "@/components/SectionHeader";
import type { User } from "@/types";

function getDisplayName(user: User): string {
  const name = [user.first_name, user.last_name].filter(Boolean).join(" ");
  return name || user.email;
}

export default function Users() {
  const { userId } = useCurrentUser();
  const [all, setAll] = useState<User[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [connecting, setConnecting] = useState<Record<number, boolean>>({});
  const [connected, setConnected] = useState<Record<number, boolean>>({});

  useEffect(() => {
    usersApi.list()
      .then(setAll)
      .finally(() => setLoading(false));
  }, []);

  const filtered = all.filter((u) => {
    if (u.id === userId) return false;
    if (!query.trim()) return true;
    const q = query.toLowerCase();
    return (
      u.email.toLowerCase().includes(q) ||
      getDisplayName(u).toLowerCase().includes(q)
    );
  });

  const handleConnect = async (id: number) => {
    setConnecting((p) => ({ ...p, [id]: true }));
    try {
      await peersApi.sendRequest(id);
      setConnected((p) => ({ ...p, [id]: true }));
    } finally {
      setConnecting((p) => ({ ...p, [id]: false }));
    }
  };

  return (
    <div className="space-y-6">
      <SectionHeader title="Find Users" />

      <div className="bg-card rounded-[20px] px-4 py-3 flex items-center gap-2">
        <svg className="w-4 h-4 text-muted-foreground shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          type="text"
          placeholder="Search by name or email..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 bg-transparent text-sm text-foreground placeholder:text-muted-foreground outline-none"
        />
        {query && (
          <button onClick={() => setQuery("")} className="text-muted-foreground hover:text-foreground">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        )}
      </div>

      {loading && (
        <div className="bg-card rounded-[20px] p-8 text-center">
          <p className="text-sm text-muted-foreground">Loading...</p>
        </div>
      )}

      {!loading && filtered.length === 0 && (
        <div className="bg-card rounded-[20px] p-8 text-center">
          <p className="text-sm text-muted-foreground">
            {query ? "No users match your search." : "No other users yet."}
          </p>
        </div>
      )}

      <div className="space-y-2">
        {filtered.map((u) => (
          <div key={u.id} className="bg-card rounded-[16px] px-4 py-3 flex items-center gap-3">
            <Link to={`/users/${u.id}`} className="w-10 h-10 rounded-full bg-accent/20 flex items-center justify-center text-accent font-bold text-sm shrink-0 hover:bg-accent/30 transition-colors">
              {u.email.charAt(0).toUpperCase()}
            </Link>
            <Link to={`/users/${u.id}`} className="flex-1 min-w-0 hover:underline">
              <div className="text-sm font-semibold text-foreground truncate">{getDisplayName(u)}</div>
              <div className="text-xs text-muted-foreground truncate">{u.email}</div>
            </Link>
            {connected[u.id] ? (
              <span className="text-xs text-muted-foreground px-3 py-1.5">Sent!</span>
            ) : (
              <button
                onClick={() => handleConnect(u.id)}
                disabled={!!connecting[u.id]}
                className="text-xs px-3 py-1.5 rounded-full bg-accent text-white disabled:opacity-50 hover:bg-accent/90 transition-colors shrink-0"
              >
                {connecting[u.id] ? "..." : "Connect"}
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
