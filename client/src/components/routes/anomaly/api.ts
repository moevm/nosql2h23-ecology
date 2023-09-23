import { AnomalyData } from "@/types/anomalies";
import axios from "axios";
import { baseURL } from "@/api";

export async function getAnomalyData(
  id: string,
  name: string,
  anomalyIndex: string
): Promise<AnomalyData> {
  return (
    await axios.get<AnomalyData>(
      baseURL + "/anomalies/" + id + "/" + name + "/" + anomalyIndex
    )
  ).data;
}
