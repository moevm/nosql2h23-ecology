import { ObjectInfo } from "@/types/objects";
import { api } from "@/api";

export async function getObjectsInfo(id: string): Promise<ObjectInfo> {
  return (
    await api.get<ObjectInfo>("/objects/object/" + id)
  ).data;
}
