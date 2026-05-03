import type { WorkoutSuggestion } from "@/types";
import { request } from "./client";

export const suggestionsApi = {
  nextWorkout: () => request<WorkoutSuggestion>("/suggestions/workout"),
};
