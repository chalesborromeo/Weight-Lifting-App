import { useState } from "react";
import { motion } from "motion/react";
import { postsApi } from "@/api/posts";
import type { Post } from "@/types";

function timeAgo(dateStr: string): string {
  const seconds = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000);
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

type Props = {
  post: Post;
  onUpdate?: (post: Post) => void;
  currentUserId: number | null;
};

export function PostCard({ post, onUpdate, currentUserId }: Props) {
  const [commentText, setCommentText] = useState("");
  const [showComments, setShowComments] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleLike = async () => {
    const updated = await postsApi.like(post.id);
    onUpdate?.(updated);
  };

  const handleComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;
    setSubmitting(true);
    try {
      await postsApi.addComment(post.id, commentText.trim());
      setCommentText("");
      // Refresh the post to get updated comments
      const updated = await postsApi.get(post.id);
      onUpdate?.(updated);
      setShowComments(true);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="border border-black/10 rounded-xl p-4 space-y-3"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-black/10 flex items-center justify-center text-xs font-medium">
            {post.user.email.charAt(0).toUpperCase()}
          </div>
          <div>
            <div className="text-sm font-medium">{post.user.email}</div>
            <div className="text-xs text-black/40">{timeAgo(post.date)}</div>
          </div>
        </div>
      </div>

      {/* Body */}
      {post.text && <p className="text-sm">{post.text}</p>}

      {post.workout_id && (
        <div className="bg-black/5 rounded-lg px-3 py-2 text-xs text-black/60">
          Workout #{post.workout_id}
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-4 pt-1">
        <button
          onClick={handleLike}
          className="flex items-center gap-1 text-sm text-black/50 hover:text-black transition-colors"
        >
          <span>{post.likes > 0 ? "❤️" : "🤍"}</span>
          <span>{post.likes}</span>
        </button>
        <button
          onClick={() => setShowComments(!showComments)}
          className="flex items-center gap-1 text-sm text-black/50 hover:text-black transition-colors"
        >
          <span>💬</span>
          <span>{post.comments.length}</span>
        </button>
      </div>

      {/* Comments */}
      {showComments && (
        <div className="space-y-2 pt-2 border-t border-black/5">
          {post.comments.map((c) => (
            <div key={c.id} className="text-sm">
              <span className="font-medium">{c.user.email}</span>{" "}
              <span className="text-black/70">{c.text}</span>
            </div>
          ))}

          {currentUserId && (
            <form onSubmit={handleComment} className="flex gap-2">
              <input
                type="text"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Add a comment..."
                className="flex-1 px-3 py-1.5 text-sm border border-black/10 rounded-full outline-none focus:border-black/30"
              />
              <button
                type="submit"
                disabled={submitting || !commentText.trim()}
                className="px-3 py-1.5 text-xs bg-black text-white rounded-full disabled:opacity-30"
              >
                Post
              </button>
            </form>
          )}
        </div>
      )}
    </motion.div>
  );
}
