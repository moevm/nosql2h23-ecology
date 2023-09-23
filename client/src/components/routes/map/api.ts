import axios from "axios";

import { baseURL } from "@/api";
import { AnomalyData } from "@/types/anomalies";

export async function getMapData(id: string): Promise<AnomalyData[]> {
  return (await axios.get<AnomalyData[]>(baseURL + "/anomalies/" + id)).data;
}
