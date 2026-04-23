import { useEffect, useState } from "react";
import { Link } from "react-router";
import { postsApi } from "@/api/posts";
import type { Post } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";
import { PostCard } from "@/components/PostCard";

export default function Feed() {
  const { userId } = useCurrentUser();
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      setPosts(await postsApi.getFeed());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load feed");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  const handlePostUpdate = (updated: Post) => {
    setPosts((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl tracking-tight">Feed</h1>
        <Link
          to="/workouts/new"
          className="px-4 py-2 bg-black text-white text-sm rounded-full"
        >
          Log Workout
        </Link>
      </div>

      {loading && <p className="text-sm text-black/60">Loading feed...</p>}
      {error && <p className="text-sm text-red-600">{error}</p>}

      {!loading && posts.length === 0 && (
        <div className="text-center py-12 space-y-3">
          <p className="text-black/50">Your feed is empty.</p>
          <p className="text-sm text-black/40">
            <Link to="/workouts/new" className="underline">Log a workout</Link> or{" "}
            <Link to="/peers" className="underline">add peers</Link> to see activity here.
          </p>
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
