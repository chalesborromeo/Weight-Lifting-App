import { useEffect, useState } from "react";
import { usersApi, peersApi } from "@/api";
import type { User, Peer } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";

export default function Peers() {
  const { userId } = useCurrentUser();
  const [peers, setPeers] = useState<Peer[]>([]);
  const [pending, setPending] = useState<Peer[]>([]);
  const [allUsers, setAllUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  async function refresh() {
    setLoading(true);
    try {
      const [p, pend, users] = await Promise.all([
        peersApi.list(),
        peersApi.pending(),
        usersApi.list(),
      ]);
      setPeers(p);
      setPending(pend);
      setAllUsers(users);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { refresh(); }, []);

  const peerIds = new Set([
    ...peers.map((p) => p.peer_id),
    ...pending.map((p) => p.user_id),
    userId,
  ]);

  const discoverable = allUsers.filter((u) => !peerIds.has(u.id));

  const handleSendRequest = async (peerId: number) => {
    await peersApi.sendRequest(peerId);
    await refresh();
  };

  const handleAccept = async (peerId: number) => {
    await peersApi.accept(peerId);
    await refresh();
  };

  const handleRemove = async (peerId: number) => {
    await peersApi.remove(peerId);
    await refresh();
  };

  if (loading) return <p className="text-sm text-black/60">Loading...</p>;

  return (
    <div className="space-y-8">
      <h1 className="text-2xl tracking-tight">Peers</h1>

      {/* Pending incoming */}
      {pending.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-sm uppercase tracking-wide text-black/60">Pending Requests</h2>
          <ul className="divide-y divide-black/10 border border-black/10 rounded-lg">
            {pending.map((p) => (
              <li key={p.id} className="px-4 py-3 flex items-center justify-between">
                <div className="text-sm">{p.user.email}</div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleAccept(p.user_id)}
                    className="px-3 py-1 text-xs bg-black text-white rounded-full"
                  >
                    Accept
                  </button>
                  <button
                    onClick={() => handleRemove(p.user_id)}
                    className="px-3 py-1 text-xs border border-black/20 rounded-full"
                  >
                    Reject
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Current peers */}
      <section className="space-y-3">
        <h2 className="text-sm uppercase tracking-wide text-black/60">
          Your Peers ({peers.length})
        </h2>
        {peers.length === 0 && (
          <p className="text-sm text-black/40">No peers yet. Add some below!</p>
        )}
        <ul className="divide-y divide-black/10 border border-black/10 rounded-lg">
          {peers.map((p) => (
            <li key={p.id} className="px-4 py-3 flex items-center justify-between">
              <div className="text-sm">{p.peer.email}</div>
              <button
                onClick={() => handleRemove(p.peer_id)}
                className="px-3 py-1 text-xs border border-black/20 rounded-full hover:border-black"
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      </section>

      {/* Discover */}
      {discoverable.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-sm uppercase tracking-wide text-black/60">Discover</h2>
          <ul className="divide-y divide-black/10 border border-black/10 rounded-lg">
            {discoverable.map((u) => (
              <li key={u.id} className="px-4 py-3 flex items-center justify-between">
                <div className="text-sm">{u.email}</div>
                <button
                  onClick={() => handleSendRequest(u.id)}
                  className="px-3 py-1 text-xs border border-black/20 rounded-full hover:border-black"
                >
                  Add Peer
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
