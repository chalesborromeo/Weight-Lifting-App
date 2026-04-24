import { useEffect, useState } from "react";
import { ApiError, usersApi } from "@/api";
import type { User } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";
import { SectionHeader } from "@/components/SectionHeader";

export default function Users() {
  const { userId, register } = useCurrentUser();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      setUsers(await usersApi.list());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load users");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { refresh(); }, []);

  async function onCreate(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await register({ email, password });
      setEmail("");
      setPassword("");
      await refresh();
    } catch (err) {
      if (err instanceof ApiError) setError(`${err.status}: ${JSON.stringify(err.body)}`);
      else setError(err instanceof Error ? err.message : "Failed to create user");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-8">
      <section className="space-y-3">
        <SectionHeader title="Users" />
        <p className="text-sm text-muted-foreground">
          Pick a user to act as. This is a placeholder for real auth.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-sm uppercase tracking-wide text-muted-foreground">Existing users</h2>
        {loading && <div className="text-sm text-muted-foreground">Loading...</div>}
        {!loading && users.length === 0 && <div className="text-sm text-muted-foreground">No users yet.</div>}
        {users.length > 0 && (
          <div className="bg-card rounded-[20px] divide-y divide-border">
            {users.map((u) => (
              <div key={u.id} className="px-4 py-3 flex items-center justify-between">
                <div>
                  <div className="text-sm text-foreground">{u.email}</div>
                  <div className="text-xs text-muted-foreground">id #{u.id}</div>
                </div>
                {userId === u.id && (
                  <span className="px-3 py-1 text-xs rounded-full bg-accent text-white">
                    You
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="space-y-3">
        <h2 className="text-sm uppercase tracking-wide text-muted-foreground">Create new user</h2>
        <form onSubmit={onCreate} className="bg-card rounded-[20px] p-6 space-y-3">
          <input
            type="email"
            required
            placeholder="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 bg-background rounded-[15px] text-sm text-foreground placeholder:text-muted-foreground outline-none focus:ring-1 focus:ring-accent"
          />
          <input
            type="password"
            required
            placeholder="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 bg-background rounded-[15px] text-sm text-foreground placeholder:text-muted-foreground outline-none focus:ring-1 focus:ring-accent"
          />
          <button
            type="submit"
            disabled={submitting}
            className="w-full px-4 py-3 bg-accent text-white rounded-[15px] disabled:opacity-50 hover:bg-accent/90 transition-colors"
          >
            {submitting ? "Creating..." : "Create user"}
          </button>
        </form>
      </section>

      {error && <div className="text-sm text-destructive">{error}</div>}
    </div>
  );
}
