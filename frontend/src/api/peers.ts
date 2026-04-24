import type { Peer } from "@/types";
import { request } from "./client";

export const peersApi = {
  list: () => request<Peer[]>("/peers/"),
  pending: () => request<Peer[]>("/peers/pending"),
  sendRequest: (peerId: number) =>
    request<Peer>(`/peers/${peerId}`, { method: "POST" }),
  accept: (peerId: number) =>
    request<Peer>(`/peers/${peerId}/accept`, { method: "PUT" }),
  remove: (peerId: number) =>
    request<void>(`/peers/${peerId}`, { method: "DELETE" }),
};
