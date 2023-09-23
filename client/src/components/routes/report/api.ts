import { AnomalyData } from "@/types/anomalies";
import axios from "axios";
import { baseURL } from "@/api";

export async function getReportData(id: string): Promise<AnomalyData[]> {
  return (await axios.get<AnomalyData[]>(baseURL + "/reports/" + id)).data;
}
