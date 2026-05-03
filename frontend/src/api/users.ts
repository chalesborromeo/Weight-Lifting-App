import type { User } from "@/types";
import { request } from "./client";

export const usersApi = {
  list: () => request<User[]>("/users/"),
  get: (id: number) => request<User>(`/users/${id}`),
  suggestions: () => request<User[]>("/users/suggestions"),
  streak: () => request<{ streak: number }>("/users/me/streak"),
  exportData: () => request<Record<string, unknown>>("/users/me/export"),
};
