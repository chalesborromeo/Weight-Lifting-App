import type { Notification } from "@/types";
import { request } from "./client";

export const notificationsApi = {
  list: () => request<Notification[]>("/notifications/"),
  markRead: (id: number) =>
    request<Notification>(`/notifications/${id}/read`, { method: "PUT" }),
};
