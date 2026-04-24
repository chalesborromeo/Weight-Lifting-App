import type { Workout, WorkoutCreate } from "@/types";
import { request } from "./client";

export const workoutsApi = {
  list: () => request<Workout[]>("/workouts/"),
  get: (id: number) => request<Workout>(`/workouts/${id}`),
  listByUser: (userId: number) => request<Workout[]>(`/workouts/user/${userId}`),
  create: (payload: WorkoutCreate) =>
    request<Workout>("/workouts/", { method: "POST", body: payload }),
  remove: (id: number) =>
    request<Workout>(`/workouts/${id}`, { method: "DELETE" }),
};
