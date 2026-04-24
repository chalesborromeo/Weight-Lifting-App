import type { SpotRequest, SpotRequestCreate } from "@/types";
import { request } from "./client";

export const spottersApi = {
  incoming: () => request<SpotRequest[]>("/spotters/incoming"),
  outgoing: () => request<SpotRequest[]>("/spotters/outgoing"),
  send: (data: SpotRequestCreate) =>
    request<SpotRequest>("/spotters/", { method: "POST", body: data }),
  accept: (id: number) =>
    request<SpotRequest>(`/spotters/${id}/accept`, { method: "PUT" }),
  decline: (id: number) =>
    request<{ message: string }>(`/spotters/${id}/decline`, { method: "DELETE" }),
};
