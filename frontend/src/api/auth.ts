import type { AuthRegister, AuthResponse, UserLogin } from "@/types";
import { request } from "./client";

export const authApi = {
  register: (payload: AuthRegister) =>
    request<AuthResponse>("/auth/register", { method: "POST", body: payload }),
  login: (payload: UserLogin) =>
    request<AuthResponse>("/auth/login", { method: "POST", body: payload }),
};
