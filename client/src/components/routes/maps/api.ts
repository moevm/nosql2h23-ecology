import { api } from "@/api";


export function deleteMap(id: string) {
  return api.delete("/images/image/" + id);
}
