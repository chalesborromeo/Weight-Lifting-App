import type { ExerciseCatalogEntry } from "@/types";
import { request } from "./client";

export const exercisesApi = {
  catalog: () => request<ExerciseCatalogEntry[]>("/exercises/catalog"),
  workoutTypes: () => request<string[]>("/exercises/workout-types"),
};
