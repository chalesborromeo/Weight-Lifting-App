import { useEffect, useState } from "react";
import { Link } from "react-router";
import { postsApi } from "@/api/posts";
import type { Post } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";
import { PostCard } from "@/components/PostCard";
import { SectionHeader } from "@/components/SectionHeader";


type FeedMode = "peers" | "global";

export default function Feed() {
  const { userId } = useCurrentUser();
  const [mode, setMode] = useState<FeedMode>("peers");
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function refresh(currentMode: FeedMode) {
    setLoading(true);
    setError(null);
    try {
      const data = currentMode === "peers"
        ? await postsApi.getFeed()
        : await postsApi.getGlobal();
      setPosts(data);
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

  return (
    <div className="space-y-4">
      <SectionHeader title="Activity Feed" />

      {/* Mode toggle */}
      <div className="flex gap-2">
        <button
          onClick={() => setMode("peers")}
          className={`px-4 py-1.5 text-xs rounded-full border transition-colors ${
            mode === "peers"
              ? "bg-accent text-white border-accent"
              : "border-inactive text-muted-foreground hover:border-foreground hover:text-foreground"
          }`}
        >
          Peers
        </button>
        <button
          onClick={() => setMode("global")}
          className={`px-4 py-1.5 text-xs rounded-full border transition-colors ${
            mode === "global"
              ? "bg-accent text-white border-accent"
              : "border-inactive text-muted-foreground hover:border-foreground hover:text-foreground"
          }`}
        >
          Global
        </button>
      </div>

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
            currentUserId={userId}
          />
        ))}
      </div>
    </div>
  );
}