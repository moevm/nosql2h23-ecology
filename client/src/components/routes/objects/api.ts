import { ObjectInfo } from "@/types/objects";
import { api } from "@/api";


export async function exportObjects() {
  return api.get<ObjectInfo[]>("/objects/impex");
}
