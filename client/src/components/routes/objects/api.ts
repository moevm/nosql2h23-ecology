import { ObjectInfo } from "@/types/objects";
import axios from "axios";
import { api, baseURL } from "@/api";

export async function getObjectsInfo(): Promise<ObjectInfo[]> {
  return (await axios.get<ObjectInfo[]>(baseURL + "/objects/")).data;
}

export async function exportObjects() {
  return api.get<ObjectInfo[]>("/objects/impex");
}
