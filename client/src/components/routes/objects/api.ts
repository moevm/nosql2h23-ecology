import { ObjectInfo } from "@/types/objects";
import axios from "axios";
import { baseURL } from "@/api";

export async function getObjectsInfo(): Promise<ObjectInfo[]> {
  return (await axios.get<ObjectInfo[]>(baseURL + "/objects/")).data;
}
