import { api } from "@/api";

export function uploadMap(file: File, name: string) {
  const formData = new FormData();
  formData.append("image", file);
  formData.append("name", name);
  return api.post("/images/upload_image", formData);
}
