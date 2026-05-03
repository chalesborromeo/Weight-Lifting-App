import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router";
import {
  ChevronRight,
  LogOut,
  Pencil,
  TrendingUp,
  Dumbbell,
} from "lucide-react";
import { profileApi, resolveAssetUrl, ApiError } from "@/api";
import { usersApi } from "@/api/users";
import { useCurrentUser } from "@/context/CurrentUser";
import { SectionHeader } from "@/components/SectionHeader";
import type { Profile as ProfileType } from "@/types";

export default function Profile() {
  const { user, logout } = useCurrentUser();
  const navigate = useNavigate();
  const [profile, setProfile] = useState<ProfileType | null>(null);
  const [streak, setStreak] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const [p, s] = await Promise.all([
          profileApi.getMine().catch((err) => {
            if (!(err instanceof ApiError && err.status === 404)) throw err;
            return null;
          }),
          usersApi.streak().catch(() => ({ streak: 0 })),
        ]);
        setProfile(p);
        setStreak(s.streak);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const displayName =
    [profile?.first_name, profile?.last_name].filter(Boolean).join(" ") ||
    user?.email ||
    "Your profile";

  const avatarUrl = resolveAssetUrl(profile?.profile_picture_url);
  const avatarInitial = user?.email.charAt(0).toUpperCase() ?? "?";

  return (
    <div className="space-y-6">
      <SectionHeader title="Profile" />

      {/* Identity header */}
      <div className="bg-card rounded-[20px] p-4 flex items-center gap-4">
        <div className="w-16 h-16 rounded-[15px] bg-background overflow-hidden ring-2 ring-accent/80 flex-shrink-0 flex items-center justify-center">
          {avatarUrl ? (
            <img src={avatarUrl} alt="" className="w-full h-full object-cover" />
          ) : (
            <span className="text-2xl font-bold text-foreground">{avatarInitial}</span>
          )}
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2 flex-wrap">
            <div className="text-lg font-semibold text-foreground truncate">{displayName}</div>
            {streak > 0 && (
              <span className="text-xs font-medium text-orange-400 bg-orange-400/10 px-2 py-0.5 rounded-full whitespace-nowrap">
                🔥 {streak} day streak
              </span>
            )}
          </div>
          <div className="text-xs text-muted-foreground truncate">{user?.email}</div>
          {profile?.bio && (
            <div className="text-xs text-muted-foreground mt-1 line-clamp-2">{profile.bio}</div>
          )}
        </div>
      </div>

      {/* Menu rows */}
      <nav className="bg-card rounded-[20px] divide-y divide-border overflow-hidden">
        <MenuRow to="/metrics" icon={<TrendingUp className="w-5 h-5" />} label="Body Metrics" />
        <MenuRow to="/spotters" icon={<Dumbbell className="w-5 h-5" />} label="Spotters" />
        <MenuRow to="/profile/edit" icon={<Pencil className="w-5 h-5" />} label="Edit Profile" />
      </nav>

      <button
        type="button"
        onClick={() => {
          logout();
          navigate("/");
        }}
        className="w-full flex items-center justify-center gap-2 text-sm text-destructive py-3"
      >
        <LogOut className="w-4 h-4" />
        Sign out
      </button>

      {loading && <div className="sr-only">Loading profile</div>}
    </div>
  );
}

function MenuRow({
  to,
  icon,
  label,
}: {
  to: string;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <Link
      to={to}
      className="flex items-center gap-3 px-4 py-4 hover:bg-background/50 transition-colors"
    >
      <span className="text-muted-foreground">{icon}</span>
      <span className="flex-1 text-foreground">{label}</span>
      <ChevronRight className="w-4 h-4 text-muted-foreground" />
    </Link>
  );
}
