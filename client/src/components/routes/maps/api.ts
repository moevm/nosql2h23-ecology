import { MapInfo } from "@/types/maps";
import axios from "axios";
import { baseURL } from "@/api";

export async function getMapsInfo(): Promise<MapInfo[]> {
  return (await axios.get<MapInfo[]>(baseURL + "/images/")).data;
}

export function deleteMap(id: string) {
  return axios.delete(baseURL + "/images/delete_image/" + id);
}
