import { ObjectData } from "@/types/objects";
import axios from "axios";
import { baseURL } from "@/api";

export async function getObjectsData(): Promise<ObjectData[]> {
  return (await axios.get<ObjectData[]>(baseURL + "/objects/")).data;
}
