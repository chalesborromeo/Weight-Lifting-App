import type { GymCheckIn, NearbyGym } from "@/types";
import { request } from "./client";

export const gymsApi = {
  nearby: (lat: number, lng: number, radius_km = 10) =>
    request<NearbyGym[]>(`/gyms/nearby?lat=${lat}&lng=${lng}&radius_km=${radius_km}`),
  listCheckins: () => request<GymCheckIn[]>("/gyms/checkins"),
  checkin: (gym_name: string, gym_address?: string | null) =>
    request<GymCheckIn>("/gyms/checkins", { method: "POST", body: { gym_name, gym_address } }),
  deleteCheckin: (id: number) =>
    request<GymCheckIn>(`/gyms/checkins/${id}`, { method: "DELETE" }),
};
