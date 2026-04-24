import { useEffect, useRef, useState } from "react";
import { Bell } from "lucide-react";
import { notificationsApi } from "@/api";
import type { Notification } from "@/types";

/**
 * Bell icon with an unread count badge and a popover list.
 * Polls on mount + on open. No real-time yet.
 */
export function NotificationBell() {
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const unreadCount = items.filter((n) => !n.read).length;

  const load = async () => {
    setLoading(true);
    try {
      setItems(await notificationsApi.list());
    } catch {
      // silently ignore — don't block the app header on a bad network
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  // Click-outside to close
  useEffect(() => {
    if (!open) return;
    const onDocClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, [open]);

  const handleToggle = () => {
    setOpen((prev) => {
      const next = !prev;
      if (next) void load();
      return next;
    });
  };

  const handleItemClick = async (n: Notification) => {
    if (n.read) return;
    // Optimistic: flip read locally, then call API
    setItems((prev) => prev.map((x) => (x.id === n.id ? { ...x, read: true } : x)));
    try {
      await notificationsApi.markRead(n.id);
    } catch {
      // roll back on failure
      setItems((prev) => prev.map((x) => (x.id === n.id ? { ...x, read: false } : x)));
    }
  };

  return (
    <div ref={containerRef} className="relative">
      <button
        onClick={handleToggle}
        aria-label={`Notifications${unreadCount > 0 ? ` (${unreadCount} unread)` : ""}`}
        className="relative w-10 h-10 rounded-full flex items-center justify-center text-foreground hover:bg-card transition-colors"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 min-w-[18px] h-[18px] px-1 rounded-full bg-destructive text-white text-[10px] font-semibold flex items-center justify-center">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-80 max-w-[calc(100vw-2rem)] bg-card rounded-[20px] shadow-xl shadow-black/20 overflow-hidden border border-border z-50">
          <div className="px-4 py-3 border-b border-border flex items-center justify-between">
            <span className="text-sm font-semibold text-foreground">Notifications</span>
            {unreadCount > 0 && (
              <span className="text-xs text-muted-foreground">
                {unreadCount} unread
              </span>
            )}
          </div>

          <div className="max-h-96 overflow-y-auto">
            {loading && items.length === 0 ? (
              <div className="px-4 py-6 text-sm text-muted-foreground text-center">
                Loading...
              </div>
            ) : items.length === 0 ? (
              <div className="px-4 py-8 text-sm text-muted-foreground text-center">
                You're all caught up.
              </div>
            ) : (
              items.map((n) => (
                <NotificationRow
                  key={n.id}
                  notification={n}
                  onClick={() => handleItemClick(n)}
                />
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function NotificationRow({
  notification,
  onClick,
}: {
  notification: Notification;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full px-4 py-3 flex items-start gap-3 text-left border-b border-border last:border-b-0 transition-colors ${
        notification.read ? "hover:bg-background/50" : "bg-accent/5 hover:bg-accent/10"
      }`}
    >
      <span
        className={`mt-1.5 w-2 h-2 rounded-full flex-shrink-0 ${
          notification.read ? "bg-transparent" : "bg-accent"
        }`}
      />
      <div className="flex-1 min-w-0">
        <div className={`text-sm ${notification.read ? "text-muted-foreground" : "text-foreground"}`}>
          {notification.message}
        </div>
        <div className="text-xs text-muted-foreground mt-0.5">
          {formatRelative(notification.time)} · {notification.type}
        </div>
      </div>
    </button>
  );
}

function formatRelative(iso: string): string {
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return "";
  const diffMs = Date.now() - then;
  const s = Math.max(0, Math.floor(diffMs / 1000));
  if (s < 60) return "just now";
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  const d = Math.floor(h / 24);
  if (d < 30) return `${d}d ago`;
  return new Date(iso).toLocaleDateString();
}
