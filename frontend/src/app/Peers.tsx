import { useEffect, useState } from "react";
import { Dumbbell, Check } from "lucide-react";
import { usersApi, peersApi, spottersApi } from "@/api";
import type { User, Peer } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";
import { SectionHeader } from "@/components/SectionHeader";

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

  const [spotRequestSent, setSpotRequestSent] = useState<Record<number, boolean>>({});
  const [spotRequestInFlight, setSpotRequestInFlight] = useState<number | null>(null);
  const handleRequestSpot = async (peerId: number) => {
    setSpotRequestInFlight(peerId);
    try {
      await spottersApi.send({ spotter_id: peerId });
      setSpotRequestSent((prev) => ({ ...prev, [peerId]: true }));
      // Clear the success indicator after a moment
      setTimeout(() => {
        setSpotRequestSent((prev) => {
          const next = { ...prev };
          delete next[peerId];
          return next;
        });
      }, 2500);
    } catch {
      // Surface failure quietly; the user can retry.
    } finally {
      setSpotRequestInFlight(null);
    }
  };

  if (loading) return <p className="text-sm text-muted-foreground">Loading...</p>;

  return (
    <div className="space-y-8">
      <SectionHeader title="Peers" />

      {/* Pending incoming */}
      {pending.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-sm uppercase tracking-wide text-muted-foreground">Pending Requests</h2>
          <div className="bg-card rounded-[20px] divide-y divide-border">
            {pending.map((p) => (
              <div key={p.id} className="px-4 py-3 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-accent text-white flex items-center justify-center text-xs font-bold">
                    {p.user.email.charAt(0).toUpperCase()}
                  </div>
                  <div className="text-sm text-foreground">{p.user.email}</div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleAccept(p.user_id)}
                    className="px-4 py-1.5 text-xs bg-accent text-white rounded-full hover:bg-accent/90 transition-colors"
                  >
                    Accept
                  </button>
                  <button
                    onClick={() => handleRemove(p.user_id)}
                    className="px-4 py-1.5 text-xs bg-card border border-inactive text-muted-foreground rounded-full hover:border-foreground hover:text-foreground transition-colors"
                  >
                    Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Current peers */}
      <section className="space-y-3">
        <h2 className="text-sm uppercase tracking-wide text-muted-foreground">
          Your Peers ({peers.length})
        </h2>
        {peers.length === 0 && (
          <p className="text-sm text-muted-foreground">No peers yet. Add some below!</p>
        )}
        {peers.length > 0 && (
          <div className="bg-card rounded-[20px] divide-y divide-border">
            {peers.map((p) => {
              const sent = spotRequestSent[p.peer_id];
              const inFlight = spotRequestInFlight === p.peer_id;
              return (
                <div key={p.id} className="px-4 py-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-accent text-white flex items-center justify-center text-xs font-bold">
                      {p.peer.email.charAt(0).toUpperCase()}
                    </div>
                    <div className="text-sm text-foreground">{p.peer.email}</div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleRequestSpot(p.peer_id)}
                      disabled={inFlight || sent}
                      aria-label={sent ? "Spot request sent" : "Request as spotter"}
                      title="Request as spotter"
                      className={`w-9 h-9 rounded-full flex items-center justify-center transition-colors ${
                        sent
                          ? "bg-emerald-500/10 text-emerald-400"
                          : "bg-card border border-accent text-accent hover:bg-accent hover:text-white"
                      } disabled:cursor-default`}
                    >
                      {sent ? <Check className="w-4 h-4" /> : <Dumbbell className="w-4 h-4" />}
                    </button>
                    <button
                      onClick={() => handleRemove(p.peer_id)}
                      className="px-4 py-1.5 text-xs bg-card border border-inactive text-muted-foreground rounded-full hover:border-foreground hover:text-foreground transition-colors"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* Discover */}
      {discoverable.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-sm uppercase tracking-wide text-muted-foreground">Discover</h2>
          <div className="bg-card rounded-[20px] divide-y divide-border">
            {discoverable.map((u) => (
              <div key={u.id} className="px-4 py-3 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-inactive text-foreground flex items-center justify-center text-xs font-bold">
                    {u.email.charAt(0).toUpperCase()}
                  </div>
                  <div className="text-sm text-foreground">{u.email}</div>
                </div>
                <button
                  onClick={() => handleSendRequest(u.id)}
                  className="px-4 py-1.5 text-xs border border-accent text-accent rounded-full hover:bg-accent hover:text-white transition-colors"
                >
                  Add Peer
                </button>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
