import type { PR, PRCreate } from "@/types";
import { request } from "./client";

export const prsApi = {
  list: () => request<PR[]>("/prs/"),
  create: (data: PRCreate) => request<PR>("/prs/", { method: "POST", body: data }),
  remove: (id: number) => request<{ message: string }>(`/prs/${id}`, { method: "DELETE" }),
  leaderboard: (exercise: string, limit = 10) =>
    request<PR[]>(`/prs/leaderboard?exercise=${encodeURIComponent(exercise)}&limit=${limit}`),
};
