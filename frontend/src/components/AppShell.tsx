import { NavLink, Outlet, useNavigate } from "react-router";
import { useCurrentUser } from "@/context/CurrentUser";

const navItems = [
  { to: "/feed", label: "Feed" },
  { to: "/workouts/new", label: "Log" },
  { to: "/workouts", label: "Workouts" },
  { to: "/clubs", label: "Clubs" },
  { to: "/peers", label: "Peers" },
];

export function AppShell() {
  const { user, logout } = useCurrentUser();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-white text-black">
      <header className="border-b border-black/10 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <NavLink to="/" className="text-lg tracking-tight">SPOTTER</NavLink>
          <nav className="flex gap-4 text-sm">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  isActive ? "text-black" : "text-black/50 hover:text-black"
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-4 text-xs">
          {user ? (
            <span className="text-black/60">{user.email}</span>
          ) : (
            <NavLink to="/login" className="text-black/60 hover:text-black">Sign In</NavLink>
          )}
          {user && (
            <button
              onClick={handleLogout}
              className="text-black/40 hover:text-black transition-colors"
            >
              Sign Out
            </button>
          )}
        </div>
      </header>
      <main className="p-6 max-w-3xl mx-auto">
        <Outlet />
      </main>
    </div>
  );
}
