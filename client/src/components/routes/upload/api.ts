import { api } from "@/api";

export function uploadMap(file: File, userId: string, name: string) {
  const formData = new FormData();
  formData.append("image", file);
  formData.append("userId", userId);
  formData.append("name", name);
  return api.post("/images/", formData);
}

export function uploadObjects(file: File, userId: string) {
  const formData = new FormData();
  formData.append("objects", file);
  formData.append("userId", userId);
  return api.post("/objects/impex", formData);
}
