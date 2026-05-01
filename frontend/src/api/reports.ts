import { request } from "./client";

export const reportsApi = {
  reportPost: (postId: number, reason: string) =>
    request<void>(`/reports/posts/${postId}`, { method: "POST", body: { reason } }),
};
