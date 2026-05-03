import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router";
import { clubsApi } from "@/api";
import type { Club, Post } from "@/types";
import { useCurrentUser } from "@/context/CurrentUser";
import { PostCard } from "@/components/PostCard";

type Tab = "feed" | "members" | "about";

export default function ClubDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { userId } = useCurrentUser();
  const [club, setClub] = useState<Club | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [tab, setTab] = useState<Tab>("feed");
  const [loading, setLoading] = useState(true);
  const [postText, setPostText] = useState("");
  const [posting, setPosting] = useState(false);

  const clubId = Number(id);
  const isMember = club ? club.members.some((m) => m.id === userId) : false;
  const isOwner = club ? club.owner.id === userId : false;

  async function loadClub() {
    setLoading(true);
    try {
      const [c, f] = await Promise.all([
        clubsApi.get(clubId),
        clubsApi.getFeed(clubId),
      ]);
      setClub(c);
      setPosts(f);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadClub();
  }, [id]);

  const handleJoin = async () => {
    if (!userId) return;
    await clubsApi.join(clubId, userId);
    await loadClub();
  };

  const handleLeave = async () => {
    if (!userId) return;
    await clubsApi.leave(clubId, userId);
    await loadClub();
  };

  const handlePost = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!postText.trim()) return;
    setPosting(true);
    try {
      await clubsApi.createPost(clubId, postText.trim());
      setPostText("");
      const feed = await clubsApi.getFeed(clubId);
      setPosts(feed);
    } finally {
      setPosting(false);
    }
  };

  const handleDelete = async () => {
    await clubsApi.remove(clubId);
    navigate("/clubs");
  };

  const handlePostUpdate = (updated: Post) => {
    setPosts((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
  };

  if (loading) {
    return <div className="text-sm text-muted-foreground p-4">Loading club...</div>;
  }

  if (!club) {
    return <div className="text-sm text-destructive p-4">Club not found</div>;
  }

  const tabs: { key: Tab; label: string }[] = [
    { key: "feed", label: "Feed" },
    { key: "members", label: `Members (${club.members.length})` },
    { key: "about", label: "About" },
  ];

  return (
    <div className="space-y-4">
      {/* Header card */}
      <div className="bg-card rounded-[20px] p-6 space-y-4">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-foreground">{club.name}</h1>
              <span className="text-[11px] bg-accent/10 text-accent px-2 py-0.5 rounded-full uppercase tracking-wide">
                {club.privacy}
              </span>
            </div>
            {club.description && (
              <p className="text-sm text-muted-foreground">{club.description}</p>
            )}
            <p className="text-xs text-muted-foreground">
              Created by {club.owner.email}
            </p>
          </div>

          {/* Stacked avatars */}
          <div className="flex -space-x-2">
            {club.members.slice(0, 5).map((m) => (
              <div
                key={m.id}
                className="w-9 h-9 rounded-full bg-accent text-white flex items-center justify-center text-[11px] font-bold border-2 border-card"
              >
                {m.email.charAt(0).toUpperCase()}
              </div>
            ))}
            {club.members.length > 5 && (
              <div className="w-9 h-9 rounded-full bg-inactive text-foreground flex items-center justify-center text-[10px] font-bold border-2 border-card">
                +{club.members.length - 5}
              </div>
            )}
          </div>
        </div>

        {/* Join / Leave */}
        {userId && !isOwner && (
          isMember ? (
            <button
              onClick={handleLeave}
              className="px-5 py-2.5 text-sm border border-inactive text-muted-foreground rounded-[15px] hover:border-foreground hover:text-foreground transition-colors"
            >
              Leave Club
            </button>
          ) : (
            <button
              onClick={handleJoin}
              className="px-5 py-2.5 text-sm bg-accent text-white rounded-[15px] hover:bg-accent/90 transition-colors"
            >
              Join Club
            </button>
          )
        )}
        {isOwner && (
          <span className="inline-block px-3 py-1 text-xs bg-accent/10 text-accent rounded-full">
            You own this club
          </span>
        )}
      </div>

      {/* Tab navigation */}
      <div className="flex gap-1 bg-card rounded-[15px] p-1">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`flex-1 py-2 text-sm rounded-[12px] transition-colors ${
              tab === t.key
                ? "bg-accent text-white font-medium"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {tab === "feed" && (
        <div className="space-y-4">
          {/* Post input */}
          {(isMember || isOwner) && (
            <form onSubmit={handlePost} className="bg-card rounded-[20px] p-4 flex gap-3">
              <input
                type="text"
                value={postText}
                onChange={(e) => setPostText(e.target.value)}
                placeholder="Write something..."
                className="flex-1 px-4 py-2.5 bg-input-background rounded-[15px] text-sm text-foreground placeholder:text-muted-foreground outline-none focus:ring-1 focus:ring-accent"
              />
              <button
                type="submit"
                disabled={posting || !postText.trim()}
                className="px-4 py-2.5 text-sm bg-accent text-white rounded-[15px] disabled:opacity-30 hover:bg-accent/90 transition-colors"
              >
                Post
              </button>
            </form>
          )}

          {posts.length === 0 && (
            <div className="bg-card rounded-[20px] p-8 text-center">
              <p className="text-sm text-muted-foreground">No posts in this club yet.</p>
            </div>
          )}

          {posts.map((post) => (
            <PostCard
              key={post.id}
              post={post}
              onUpdate={handlePostUpdate}
              currentUserId={userId}
            />
          ))}
        </div>
      )}

      {tab === "members" && (
        <div className="bg-card rounded-[20px] divide-y divide-border">
          {/* Owner first */}
          <div className="px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-accent text-white flex items-center justify-center text-sm font-bold">
                {club.owner.email.charAt(0).toUpperCase()}
              </div>
              <div>
                <div className="text-sm font-medium text-foreground">{club.owner.email}</div>
                <div className="text-xs text-muted-foreground">Owner</div>
              </div>
            </div>
            <span className="px-2.5 py-0.5 text-[11px] bg-accent/10 text-accent rounded-full">
              Owner
            </span>
          </div>

          {/* Members */}
          {club.members
            .filter((m) => m.id !== club.owner.id)
            .map((m) => (
              <div key={m.id} className="px-4 py-3 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-inactive text-foreground flex items-center justify-center text-sm font-bold">
                    {m.email.charAt(0).toUpperCase()}
                  </div>
                  <div className="text-sm text-foreground">{m.email}</div>
                </div>
                {isOwner && m.id !== userId && (
                  <button
                    onClick={async () => {
                      await clubsApi.leave(clubId, m.id);
                      await loadClub();
                    }}
                    className="px-3 py-1 text-xs border border-inactive text-muted-foreground rounded-full hover:border-destructive hover:text-destructive transition-colors"
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}

          {club.members.length === 0 && (
            <div className="px-4 py-8 text-center">
              <p className="text-sm text-muted-foreground">No members yet.</p>
            </div>
          )}
        </div>
      )}

      {tab === "about" && (
        <div className="bg-card rounded-[20px] p-6 space-y-4">
          <div className="space-y-3">
            <div>
              <div className="text-xs text-muted-foreground uppercase tracking-wide">Description</div>
              <p className="text-sm text-foreground mt-1">
                {club.description || "No description."}
              </p>
            </div>
            <div>
              <div className="text-xs text-muted-foreground uppercase tracking-wide">Created by</div>
              <p className="text-sm text-foreground mt-1">{club.owner.email}</p>
            </div>
            <div>
              <div className="text-xs text-muted-foreground uppercase tracking-wide">Privacy</div>
              <p className="text-sm text-foreground mt-1 capitalize">{club.privacy}</p>
            </div>
            <div>
              <div className="text-xs text-muted-foreground uppercase tracking-wide">Members</div>
              <p className="text-sm text-foreground mt-1">{club.members.length}</p>
            </div>
          </div>

          {isOwner && (
            <div className="pt-4 border-t border-border">
              <button
                onClick={handleDelete}
                className="px-4 py-2.5 text-sm bg-destructive text-white rounded-[15px] hover:bg-destructive/90 transition-colors"
              >
                Delete Club
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
