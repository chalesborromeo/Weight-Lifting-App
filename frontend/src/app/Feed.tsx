import { useEffect, useState } from "react";
import { Link } from "react-router";
import { postsApi } from "@/api/posts";
import type { Post } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";
import { PostCard } from "@/components/PostCard";
import { SectionHeader } from "@/components/SectionHeader";

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
    <div className="space-y-4">
      <SectionHeader title="Activity Feed" />

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
          <div className="w-16 h-16 mx-auto rounded-full bg-accent/10 flex items-center justify-center">
            <svg className="w-8 h-8 text-accent" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29z"/>
            </svg>
          </div>
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
