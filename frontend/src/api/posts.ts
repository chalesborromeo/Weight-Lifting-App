import type { Post, PostCreate, Comment } from "@/types";
import { request } from "./client";

export const postsApi = {
  getFeed: () => request<Post[]>("/posts/feed"),
  getGlobal: () => request<Post[]>("/posts/global"),
  create: (payload: PostCreate) =>
    request<Post>("/posts/", { method: "POST", body: payload }),
  get: (id: number) => request<Post>(`/posts/${id}`),
  like: (id: number) =>
    request<Post>(`/posts/${id}/like`, { method: "POST" }),
  addComment: (postId: number, text: string) =>
    request<Comment>(`/posts/${postId}/comments`, { method: "POST", body: { text } }),
  getComments: (postId: number) =>
    request<Comment[]>(`/posts/${postId}/comments`),
  update: (id: number, text: string) =>
    request<Post>(`/posts/${id}`, { method: "PATCH", body: { text } }),
  remove: (id: number) =>
    request<Post>(`/posts/${id}`, { method: "DELETE" }),
};
