import type { FavoriteExercise } from "@/types";
import { request } from "./client";

export const favoriteExercisesApi = {
  list: () => request<FavoriteExercise[]>("/favorite-exercises/"),
  add: (name: string) =>
    request<FavoriteExercise>("/favorite-exercises/", { method: "POST", body: { name } }),
  remove: (id: number) =>
    request<void>(`/favorite-exercises/${id}`, { method: "DELETE" }),
};
