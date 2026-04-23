import type { Club, ClubCreate } from "@/types";
import { request } from "./client";

export const clubsApi = {
  list: () => request<Club[]>("/clubs/"),
  get: (id: number) => request<Club>(`/clubs/${id}`),
  create: (payload: ClubCreate) =>
    request<Club>("/clubs/", { method: "POST", body: payload }),
  remove: (id: number) =>
    request<Club>(`/clubs/${id}`, { method: "DELETE" }),
  join: (clubId: number, memberId: number) =>
    request<Club>(`/clubs/${clubId}/member/${memberId}`, { method: "POST" }),
  leave: (clubId: number, memberId: number) =>
    request<Club>(`/clubs/${clubId}/member/${memberId}`, { method: "DELETE" }),
};
