import axios from "axios";

import { baseURL } from "@/api";
import { ObjectData } from "@/types/objects";

export async function getMapData(id: string): Promise<ObjectData[]> {
  return (await axios.get<ObjectData[]>(baseURL + "/objects/" + id)).data;
}