import type { NearbyGym } from "@/types";
import { request } from "./client";

export const gymsApi = {
  nearby: (lat: number, lng: number, radius_km = 10) =>
    request<NearbyGym[]>(
      `/gyms/nearby?lat=${lat}&lng=${lng}&radius_km=${radius_km}`,
    ),
};
