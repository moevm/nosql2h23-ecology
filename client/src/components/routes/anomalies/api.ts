import { AnomalyData } from "@/types/anomalies";
import axios from "axios";
import { baseURL } from "@/api";

export async function getAnomaliesInfo(): Promise<AnomalyData[]> {
  return (await axios.get<AnomalyData[]>(baseURL + "/anomalies/")).data;
}
