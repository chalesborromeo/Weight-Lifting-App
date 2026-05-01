import { useState } from "react";
import { postsApi } from "@/api/posts";
import { reportsApi } from "@/api/reports";
import type { Post, Workout } from "@/types";

function timeAgo(dateStr: string): string {
  const seconds = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000);
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days}d`;
  return new Date(dateStr).toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function formatDuration(mins: number): string {
  const h = Math.floor(mins / 60);
  const m = Math.round(mins % 60);
  return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

function calcVolume(workout: Workout): number {
  let total = 0;
  for (const ex of workout.exercises) {
    for (const s of ex.sets) {
      total += s.weight * s.reps;
    }
  }
  return total;
}

function formatVolume(lbs: number): string {
  if (lbs >= 1000) return `${(lbs / 1000).toFixed(1)}k`;
  return String(lbs);
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
  const [liked, setLiked] = useState(false);
  const [showReportForm, setShowReportForm] = useState(false);
  const [reportReason, setReportReason] = useState("");
  const [reportSubmitting, setReportSubmitting] = useState(false);
  const [reported, setReported] = useState(false);

  const workout = post.workout;
  const totalSets = workout
    ? workout.exercises.reduce((sum, ex) => sum + ex.sets.length, 0)
    : 0;
  const volume = workout ? calcVolume(workout) : 0;

  const handleLike = async () => {
    if (liked) return;
    setLiked(true);
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
      const updated = await postsApi.get(post.id);
      onUpdate?.(updated);
      setShowComments(true);
    } finally {
      setSubmitting(false);
    }
  };

  const handleReport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reportReason.trim()) return;
    setReportSubmitting(true);
    try {
      await reportsApi.reportPost(post.id, reportReason.trim());
      setReported(true);
      setShowReportForm(false);
      setReportReason("");
    } finally {
      setReportSubmitting(false);
    }
  };

  return (
    <div className="bg-card rounded-[20px] overflow-hidden">
      {/* Header — user info */}
      <div className="px-4 pt-4 pb-3 flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-accent flex items-center justify-center text-white text-sm font-bold shrink-0">
          {post.user.email.charAt(0).toUpperCase()}
        </div>
        <div className="min-w-0">
          <div className="text-sm font-semibold text-foreground truncate">
            {post.user.email}
          </div>
          <div className="text-xs text-muted-foreground">
            {timeAgo(post.date)} ago
          </div>
        </div>
      </div>

      {/* Activity title */}
      {workout && (
        <div className="px-4 pb-2">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-foreground shrink-0" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29z"/>
            </svg>
            <h3 className="text-base font-semibold text-foreground">
              {workout.name}
            </h3>
          </div>
          {post.text && workout.name && !post.text.includes(workout.name) && (
            <p className="text-sm text-muted-foreground mt-1">{post.text}</p>
          )}
        </div>
      )}

      {!workout && post.text && (
        <div className="px-4 pb-2">
          <p className="text-sm text-foreground">{post.text}</p>
        </div>
      )}

      {/* Stats row */}
      {workout && (
        <div className="px-4 pb-3">
          <div className="grid grid-cols-4 gap-3 py-3 border-y border-border">
            <div>
              <div className="text-lg font-semibold text-foreground">
                {formatDuration(workout.duration)}
              </div>
              <div className="text-[11px] text-muted-foreground uppercase tracking-wide">
                Duration
              </div>
            </div>
            <div>
              <div className="text-lg font-semibold text-foreground">
                {workout.exercises.length}
              </div>
              <div className="text-[11px] text-muted-foreground uppercase tracking-wide">
                Exercises
              </div>
            </div>
            <div>
              <div className="text-lg font-semibold text-foreground">
                {totalSets}
              </div>
              <div className="text-[11px] text-muted-foreground uppercase tracking-wide">
                Sets
              </div>
            </div>
            <div>
              <div className="text-lg font-semibold text-foreground">
                {formatVolume(volume)}
              </div>
              <div className="text-[11px] text-muted-foreground uppercase tracking-wide">
                Volume (lbs)
              </div>
            </div>
          </div>

          {/* Exercise preview */}
          <div className="pt-3 space-y-1">
            {workout.exercises.slice(0, 3).map((ex) => (
              <div key={ex.id} className="flex items-center justify-between text-sm">
                <span className="text-foreground">{ex.name}</span>
                <span className="text-muted-foreground text-xs">
                  {ex.sets.length} sets &middot; {Math.max(...ex.sets.map((s) => s.weight))} lbs
                </span>
              </div>
            ))}
            {workout.exercises.length > 3 && (
              <div className="text-xs text-muted-foreground">
                +{workout.exercises.length - 3} more exercises
              </div>
            )}
          </div>
        </div>
      )}

      {/* Kudos & Comments bar */}
      <div className="px-4 py-2.5 border-t border-border flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={handleLike}
            className={`flex items-center gap-1.5 text-sm transition-colors ${
              liked || post.likes > 0
                ? "text-accent"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill={liked || post.likes > 0 ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
            {post.likes > 0 && <span>{post.likes}</span>}
          </button>
          <button
            onClick={() => setShowComments(!showComments)}
            className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            {post.comments.length > 0 && <span>{post.comments.length}</span>}
          </button>
          {currentUserId && post.user_id !== currentUserId && (
            <button
              onClick={() => !reported && setShowReportForm((v) => !v)}
              disabled={reported}
              className={`flex items-center gap-1.5 text-sm transition-colors ${
                reported
                  ? "text-muted-foreground cursor-default"
                  : "text-muted-foreground hover:text-destructive"
              }`}
              aria-label="Report post"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/>
                <line x1="4" y1="22" x2="4" y2="15"/>
              </svg>
              <span className="text-xs">{reported ? "Reported" : "Report"}</span>
            </button>
          )}
        </div>
        {post.workout && (
          <span className="text-xs text-accent bg-accent/10 px-2.5 py-1 rounded-full uppercase tracking-wide">
            {post.workout.type}
          </span>
        )}
      </div>

      {/* Report form */}
      {showReportForm && (
        <form onSubmit={handleReport} className="px-4 pb-4 border-t border-border pt-3 space-y-2">
          <p className="text-xs text-muted-foreground">Why are you reporting this post?</p>
          <input
            value={reportReason}
            onChange={(e) => setReportReason(e.target.value)}
            placeholder="e.g. Spam, inappropriate content..."
            autoFocus
            className="w-full px-3 py-2 text-sm bg-background rounded-[12px] outline-none focus:ring-1 focus:ring-accent transition-colors"
          />
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => { setShowReportForm(false); setReportReason(""); }}
              className="flex-1 px-4 py-2 text-xs text-muted-foreground bg-background rounded-[12px]"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!reportReason.trim() || reportSubmitting}
              className="flex-1 px-4 py-2 text-xs font-medium bg-destructive text-white rounded-[12px] disabled:opacity-40"
            >
              {reportSubmitting ? "Submitting..." : "Submit Report"}
            </button>
          </div>
        </form>
      )}

      {/* Comments section */}
      {showComments && (
        <div className="px-4 pb-4 border-t border-border pt-3 space-y-3">
          {post.comments.length === 0 && (
            <p className="text-xs text-muted-foreground">No comments yet. Be the first!</p>
          )}
          {post.comments.map((c) => (
            <div key={c.id} className="flex gap-2">
              <div className="w-6 h-6 rounded-full bg-inactive flex items-center justify-center text-[10px] font-bold text-foreground shrink-0 mt-0.5">
                {c.user.email.charAt(0).toUpperCase()}
              </div>
              <div>
                <span className="text-sm font-medium text-foreground">{c.user.email}</span>{" "}
                <span className="text-sm text-muted-foreground">{c.text}</span>
              </div>
            </div>
          ))}

          {currentUserId && (
            <form onSubmit={handleComment} className="flex gap-2 pt-1">
              <input
                type="text"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Add a comment..."
                className="flex-1 px-3 py-2 text-sm bg-background rounded-[15px] outline-none focus:ring-1 focus:ring-accent transition-colors"
              />
              <button
                type="submit"
                disabled={submitting || !commentText.trim()}
                className="px-4 py-2 text-xs font-medium bg-accent text-white rounded-[15px] disabled:opacity-30 hover:bg-accent/90 transition-colors"
              >
                Post
              </button>
            </form>
          )}
        </div>
      )}
    </div>
  );
}
