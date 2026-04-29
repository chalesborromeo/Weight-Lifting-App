import type { FavoriteExercise } from "@/types";
import { request } from "./client";

export const favoriteExerciseApi={
    list:()=>request<FavoriteExercise[]>("/favorite-exercises/"),
    add: (name:string)=>request<FavoriteExercise>("/favorite-exercises/",{
        method: "POST",
        body: JSON.stringify({name}),
    }),
    remove: (id: number)=> request<void>(`/favorite-exercises/${id}`,{
        method: "DELETE",
    })
};