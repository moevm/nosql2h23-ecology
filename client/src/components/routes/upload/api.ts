import { api } from "@/api";

export function uploadMap(file: File, name: string) {
  const formData = new FormData();
  formData.append("map", file);
  formData.append("name", name);
  return api.post("/maps/upload_map", formData);
}
