import { useEffect, useRef, useState } from "react";
import { NavLink, Outlet, useLocation } from "react-router";
import { Heart, Plus, Trophy, User, CircleUser, Menu, X } from "lucide-react";
import { useCurrentUser } from "@/context/CurrentUser";
import { ThemeToggle } from "@/components/ThemeToggle";
import { NotificationBell } from "@/components/NotificationBell";

const NAV_ITEMS = [
  { to: "/feed", label: "Feed" },
  { to: "/workouts", label: "Workouts" },
  { to: "/prs", label: "PRs" },
  { to: "/stats", label: "Stats" },
  { to: "/clubs", label: "Clubs" },
  { to: "/peers", label: "Peers" },
  { to: "/stats", label: "Stats" },
  { to: "/suggested-workout", label: "Suggested Workout" },
  { to: "/exercise-history", label: "Exercise History" },
  { to: "/metrics", label: "Body Metrics" },
  { to: "/spotters", label: "Spotters" },
  { to: "/gyms", label: "Gyms" },
  { to: "/favorites", label: "Favorites" },
  { to: "/users", label: "Find Users" },
];

export function AppShell() {
  const { user } = useCurrentUser();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const location = useLocation();

  // Close menu on navigation
  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  // Close menu when clicking outside
  useEffect(() => {
    if (!menuOpen) return;
    function handleClick(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [menuOpen]);

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-background/95 backdrop-blur-md border-b border-border">
        <div className="max-w-2xl mx-auto px-6 py-4 flex items-center justify-between">
          <NavLink to="/feed" className="text-xl font-bold tracking-tight text-foreground">
            SPOTTER
          </NavLink>

          <div className="flex items-center gap-3">
            <ThemeToggle />
            {user && <NotificationBell />}
            {user ? (
              <NavLink
                to="/profile"
                className="w-[40px] h-[40px] rounded-full bg-accent flex items-center justify-center text-white text-sm font-bold shrink-0"
                aria-label="Profile"
              >
                {user.email.charAt(0).toUpperCase()}
              </NavLink>
            ) : (
              <NavLink
                to="/login"
                className="px-4 py-2 text-sm bg-accent text-white rounded-[15px] hover:bg-accent/90 transition-colors"
              >
                Sign In
              </NavLink>
            )}

            {/* Hamburger */}
            <div className="relative" ref={menuRef}>
              <button
                onClick={() => setMenuOpen((v) => !v)}
                className="w-[40px] h-[40px] flex items-center justify-center rounded-full bg-card text-foreground hover:bg-accent/10 transition-colors"
                aria-label="Open menu"
              >
                {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>

              {menuOpen && (
                <div className="absolute right-0 top-12 w-52 bg-card border border-border rounded-[20px] shadow-lg overflow-hidden z-50">
                  {NAV_ITEMS.map((item) => (
                    <NavLink
                      key={item.to}
                      to={item.to}
                      className={({ isActive }) =>
                        `block px-5 py-3 text-sm transition-colors ${
                          isActive
                            ? "bg-accent/10 text-accent font-medium"
                            : "text-foreground hover:bg-accent/5"
                        }`
                      }
                    >
                      {item.label}
                    </NavLink>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-2xl mx-auto px-6 py-6 pb-28">
        <Outlet />
      </main>

      {/* Bottom Nav */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-md border-t border-border">
        <div className="max-w-2xl mx-auto flex items-center justify-around py-3 px-6">
          <NavLink
            to="/feed"
            className={({ isActive }) =>
              `flex flex-col items-center transition-colors ${
                isActive ? "text-foreground" : "text-muted-foreground"
              }`
            }
            aria-label="Feed"
          >
            <Heart className="w-6 h-6" />
          </NavLink>

          <NavLink
            to="/prs"
            className={({ isActive }) =>
              `flex flex-col items-center transition-colors ${
                isActive ? "text-foreground" : "text-muted-foreground"
              }`
            }
            aria-label="PRs"
          >
            <Trophy className="w-6 h-6" />
          </NavLink>

          <NavLink
            to="/workouts/new"
            className="w-14 h-14 rounded-full bg-accent flex items-center justify-center text-white -mt-6 shadow-lg shadow-accent/30"
            aria-label="New workout"
          >
            <Plus className="w-6 h-6" />
          </NavLink>

          <NavLink
            to="/peers"
            className={({ isActive }) =>
              `flex flex-col items-center transition-colors ${
                isActive ? "text-foreground" : "text-muted-foreground"
              }`
            }
            aria-label="Peers"
          >
            <User className="w-6 h-6" />
          </NavLink>

          <NavLink
            to="/profile"
            className={({ isActive }) =>
              `flex flex-col items-center transition-colors ${
                isActive ? "text-foreground" : "text-muted-foreground"
              }`
            }
            aria-label="Profile"
          >
            <CircleUser className="w-6 h-6" />
          </NavLink>
        </div>
      </nav>
    </div>
  );
}
