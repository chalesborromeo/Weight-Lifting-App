import { useEffect, useState } from "react";
import { Check, X, Dumbbell, Clock } from "lucide-react";
import { spottersApi } from "@/api";
import { SectionHeader } from "@/components/SectionHeader";
import type { SpotRequest } from "@/types";

type Tab = "incoming" | "outgoing";

export default function Spotters() {
  const [tab, setTab] = useState<Tab>("incoming");
  const [incoming, setIncoming] = useState<SpotRequest[]>([]);
  const [outgoing, setOutgoing] = useState<SpotRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [inc, out] = await Promise.all([spottersApi.incoming(), spottersApi.outgoing()]);
      setIncoming(inc);
      setOutgoing(out);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load spot requests");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadAll();
  }, []);

  const handleAccept = async (id: number) => {
    const previous = incoming;
    // Optimistic: flip status
    setIncoming((prev) => prev.map((r) => (r.id === id ? { ...r, status: true } : r)));
    try {
      await spottersApi.accept(id);
    } catch {
      setIncoming(previous);
      setError("Failed to accept");
    }
  };

  const handleDecline = async (id: number) => {
    const previous = incoming;
    setIncoming((prev) => prev.filter((r) => r.id !== id));
    try {
      await spottersApi.decline(id);
    } catch {
      setIncoming(previous);
      setError("Failed to decline");
    }
  };

  const pendingIncoming = incoming.filter((r) => !r.status).length;

  return (
    <div className="space-y-6">
      <SectionHeader title="Spotters" />

      <div className="flex gap-1 bg-card rounded-[15px] p-1">
        <TabButton active={tab === "incoming"} onClick={() => setTab("incoming")}>
          Incoming {pendingIncoming > 0 && <Badge>{pendingIncoming}</Badge>}
        </TabButton>
        <TabButton active={tab === "outgoing"} onClick={() => setTab("outgoing")}>
          Outgoing
        </TabButton>
      </div>

      {loading && <div className="text-sm text-muted-foreground">Loading...</div>}
      {error && <div className="text-sm text-destructive">{error}</div>}

      {tab === "incoming" ? (
        <IncomingList
          requests={incoming}
          onAccept={handleAccept}
          onDecline={handleDecline}
        />
      ) : (
        <OutgoingList requests={outgoing} />
      )}
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
      className={`flex-1 px-4 py-2 text-sm rounded-[12px] transition-colors flex items-center justify-center gap-2 ${
        active ? "bg-accent text-white" : "text-muted-foreground hover:text-foreground"
      }`}
    >
      {children}
    </button>
  );
}

function Badge({ children }: { children: React.ReactNode }) {
  return (
    <span className="min-w-[18px] h-[18px] px-1.5 rounded-full bg-destructive text-white text-[10px] font-semibold flex items-center justify-center">
      {children}
    </span>
  );
}

function IncomingList({
  requests,
  onAccept,
  onDecline,
}: {
  requests: SpotRequest[];
  onAccept: (id: number) => void;
  onDecline: (id: number) => void;
}) {
  if (requests.length === 0) {
    return (
      <div className="bg-card rounded-[20px] p-8 text-center text-sm text-muted-foreground">
        No spot requests coming your way.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {requests.map((r) => (
        <div key={r.id} className="bg-card rounded-[20px] p-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-accent flex items-center justify-center text-white font-semibold">
              {r.requester.email.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-semibold text-foreground truncate">
                {r.requester.email}
              </div>
              <div className="text-xs text-muted-foreground mt-0.5 flex items-center gap-1">
                <Dumbbell className="w-3 h-3" />
                wants you as a spotter
              </div>
            </div>
            {r.status ? (
              <span className="text-xs px-2.5 py-1 rounded-[10px] bg-emerald-500/10 text-emerald-400">
                accepted
              </span>
            ) : (
              <div className="flex gap-2">
                <button
                  onClick={() => onDecline(r.id)}
                  aria-label="Decline"
                  className="w-9 h-9 rounded-full bg-background hover:bg-destructive/10 text-destructive flex items-center justify-center transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
                <button
                  onClick={() => onAccept(r.id)}
                  aria-label="Accept"
                  className="w-9 h-9 rounded-full bg-accent hover:bg-accent/90 text-white flex items-center justify-center transition-colors"
                >
                  <Check className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

function OutgoingList({ requests }: { requests: SpotRequest[] }) {
  if (requests.length === 0) {
    return (
      <div className="bg-card rounded-[20px] p-8 text-center text-sm text-muted-foreground">
        You haven't requested any spots yet. Head to Peers and tap the dumbbell icon.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {requests.map((r) => (
        <div key={r.id} className="bg-card rounded-[20px] p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-inactive flex items-center justify-center text-white font-semibold">
            {r.spotter.email.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-semibold text-foreground truncate">
              {r.spotter.email}
            </div>
            <div className="text-xs text-muted-foreground mt-0.5">requested as spotter</div>
          </div>
          {r.status ? (
            <span className="text-xs px-2.5 py-1 rounded-[10px] bg-emerald-500/10 text-emerald-400">
              accepted
            </span>
          ) : (
            <span className="text-xs px-2.5 py-1 rounded-[10px] bg-inactive/20 text-muted-foreground flex items-center gap-1">
              <Clock className="w-3 h-3" />
              pending
            </span>
          )}
        </div>
      ))}
    </div>
  );
}
