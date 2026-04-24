import type { Profile, ProfileUpdate } from "@/types";
import { request } from "./client";

export const profileApi = {
  getMine: () => request<Profile>("/profiles/me"),
  create: (data: ProfileUpdate) => request<Profile>("/profiles/me", { method: "POST", body: data }),
  update: (data: ProfileUpdate) => request<Profile>("/profiles/me", { method: "PUT", body: data }),
  setGym: (gymId: number) => request<Profile>(`/profiles/me/gym/${gymId}`, { method: "PUT" }),
  uploadPicture: (file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    return request<Profile>("/profiles/me/picture", { method: "POST", body: fd });
  },
};
