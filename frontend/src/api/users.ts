import type { User } from "@/types";
import { request } from "./client";

export const usersApi = {
  list: () => request<User[]>("/users/"),
  get: (id: number) => request<User>(`/users/${id}`),
};
