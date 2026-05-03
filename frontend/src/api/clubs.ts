import type { Club, ClubCreate, Post } from "@/types";
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
  getFeed: (clubId: number) =>
    request<Post[]>(`/clubs/${clubId}/feed`),
  createPost: (clubId: number, text: string) =>
    request<Post>(`/clubs/${clubId}/posts`, { method: "POST", body: { text } }),
};
