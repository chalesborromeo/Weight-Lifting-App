import { createContext, useContext, useState, type ReactNode } from "react";
import { setStoredToken } from "@/api/client";
import { authApi } from "@/api/auth";
import type { User, AuthRegister, UserLogin } from "@/types";

const USER_KEY = "currentUser";

type AuthContextValue = {
  userId: number | null;
  user: User | null;
  login: (data: UserLogin) => Promise<void>;
  register: (data: AuthRegister) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function loadStoredUser(): User | null {
  const raw = typeof window !== "undefined" ? window.localStorage.getItem(USER_KEY) : null;
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return null; }
}

export function CurrentUserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(loadStoredUser);

  const saveUser = (u: User | null) => {
    setUser(u);
    if (u) window.localStorage.setItem(USER_KEY, JSON.stringify(u));
    else window.localStorage.removeItem(USER_KEY);
  };

  const login = async (data: UserLogin) => {
    const res = await authApi.login(data);
    setStoredToken(res.access_token);
    saveUser(res.user);
  };

  const register = async (data: AuthRegister) => {
    const res = await authApi.register(data);
    setStoredToken(res.access_token);
    saveUser(res.user);
  };

  const logout = () => {
    setStoredToken(null);
    saveUser(null);
  };

  return (
    <AuthContext.Provider value={{ userId: user?.id ?? null, user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useCurrentUser() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useCurrentUser must be used inside CurrentUserProvider");
  return ctx;
}
