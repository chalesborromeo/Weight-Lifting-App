import { useEffect, useState } from "react";
import { Link } from "react-router";
import { postsApi } from "@/api/posts";
import { peersApi } from "@/api/peers";
import { usersApi } from "@/api/users";
import type { Post, User } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";
import { PostCard } from "@/components/PostCard";
import { SectionHeader } from "@/components/SectionHeader";

function getDisplayName(user: User): string {
  const name = [user.first_name, user.last_name].filter(Boolean).join(" ");
  return name || user.email;
}

function SuggestionCard({ user, onConnect }: { user: User; onConnect: (id: number) => void }) {
  const [sent, setSent] = useState(false);

  const handleConnect = async () => {
    setSent(true);
    try {
      await peersApi.sendRequest(user.id);
      onConnect(user.id);
    } catch {
      setSent(false);
    }
  };

  return (
    <div className="flex-shrink-0 w-36 bg-card rounded-[16px] p-3 flex flex-col items-center gap-2 text-center">
      <div className="w-12 h-12 rounded-full bg-accent/20 flex items-center justify-center text-accent font-bold text-lg">
        {user.email.charAt(0).toUpperCase()}
      </div>
      <div className="w-full">
        <p className="text-xs font-semibold text-foreground truncate">{getDisplayName(user)}</p>
        <p className="text-[10px] text-muted-foreground truncate">{user.email}</p>
      </div>
      <button
        onClick={handleConnect}
        disabled={sent}
        className="w-full py-1.5 text-xs font-medium rounded-full bg-accent text-white disabled:opacity-50 disabled:cursor-default transition-opacity"
      >
        {sent ? "Sent!" : "Connect"}
      </button>
    </div>
  );
}

type FeedMode = "peers" | "global";

export default function Feed() {
  const { userId } = useCurrentUser();
  const [mode, setMode] = useState<FeedMode>("peers");
  const [posts, setPosts] = useState<Post[]>([]);
  const [suggestions, setSuggestions] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function refresh(currentMode: FeedMode) {
    setLoading(true);
    setError(null);
    try {
      const [feedPosts, suggested] = await Promise.all([
        postsApi.getFeed(),
        usersApi.suggestions().catch(() => [] as User[]),
      ]);
      setPosts(feedPosts);
      setSuggestions(suggested);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load feed");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh(mode);
  }, [mode]);

  const handlePostUpdate = (updated: Post) => {
    setPosts((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
  };

  const handlePostDelete = (postId: number) => {
    setPosts((prev) => prev.filter((p) => p.id !== postId));
  };

  const handleConnected = (connectedId: number) => {
    setSuggestions((prev) => prev.filter((u) => u.id !== connectedId));
  };

  return (
    <div className="space-y-4">
      <SectionHeader title="Activity Feed" />

      {/* People you might know */}
      {suggestions.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide px-1">
            People you might know
          </p>
          <div className="flex gap-3 overflow-x-auto pb-1 -mx-4 px-4 scrollbar-none">
            {suggestions.map((user) => (
              <SuggestionCard key={user.id} user={user} onConnect={handleConnected} />
            ))}
          </div>
        </div>
      )}

      {loading && (
        <div className="bg-card rounded-[20px] p-8 text-center">
          <p className="text-sm text-muted-foreground">Loading your feed...</p>
        </div>
      )}
      {error && (
        <div className="bg-destructive/10 rounded-[20px] p-4 text-center">
          <p className="text-sm text-destructive">{error}</p>
        </div>
      )}

      {!loading && posts.length === 0 && (
        <div className="bg-card rounded-[20px] p-12 text-center space-y-4">
          <div>
            <p className="text-foreground font-medium">No activity yet</p>
            <p className="text-sm text-muted-foreground mt-1">
              <Link to="/workouts/new" className="text-accent hover:underline">Log a workout</Link> or{" "}
              <Link to="/peers" className="text-accent hover:underline">find peers</Link> to see activity here.
            </p>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            onUpdate={handlePostUpdate}
            onDelete={handlePostDelete}
            currentUserId={userId}
          />
        ))}
      </div>
    </div>
  );
}