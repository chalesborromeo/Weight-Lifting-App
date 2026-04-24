import { useEffect, useState } from "react";
import { ApiError, usersApi } from "@/api";
import type { User } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";

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
        <h1 className="text-2xl tracking-tight">Users</h1>
        <p className="text-sm text-black/60">
          Pick a user to act as. This is a placeholder for real auth.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-sm uppercase tracking-wide text-black/60">Existing users</h2>
        {loading && <div className="text-sm text-black/60">Loading…</div>}
        {!loading && users.length === 0 && <div className="text-sm text-black/60">No users yet.</div>}
        <ul className="divide-y divide-black/10 border border-black/10 rounded-lg">
          {users.map((u) => (
            <li key={u.id} className="px-4 py-3 flex items-center justify-between">
              <div>
                <div className="text-sm">{u.email}</div>
                <div className="text-xs text-black/50">id #{u.id}</div>
              </div>
              {userId === u.id && (
                <span className="px-3 py-1 text-xs rounded-full bg-black text-white">
                  You
                </span>
              )}
            </li>
          ))}
        </ul>
      </section>

      <section className="space-y-3">
        <h2 className="text-sm uppercase tracking-wide text-black/60">Create new user</h2>
        <form onSubmit={onCreate} className="space-y-3">
          <input
            type="email"
            required
            placeholder="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border border-black/20 rounded-md text-sm"
          />
          <input
            type="password"
            required
            placeholder="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2 border border-black/20 rounded-md text-sm"
          />
          <button
            type="submit"
            disabled={submitting}
            className="px-4 py-2 bg-black text-white text-sm rounded-md disabled:opacity-50"
          >
            {submitting ? "Creating…" : "Create user"}
          </button>
        </form>
      </section>

      {error && <div className="text-sm text-red-600">{error}</div>}
    </div>
  );
}
