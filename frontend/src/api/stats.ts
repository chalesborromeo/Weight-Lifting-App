import type { WorkoutStats, PeriodicVolume } from "@/types";
import { request } from "./client";

function fmt(d: Date) {
  return d.toISOString();
}

export const statsApi = {
  overview: (start: Date, end: Date) =>
    request<WorkoutStats>(
      `/stats/overview?start_date=${fmt(start)}&end_date=${fmt(end)}`
    ),
  periodic: (start: Date, end: Date) =>
    request<PeriodicVolume[]>(
      `/stats/volume/periodic?start_date=${fmt(start)}&end_date=${fmt(end)}&period=week`
    ),
};
