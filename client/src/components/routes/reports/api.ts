import { ReportInfo } from "@/types/reports";
import axios from "axios";
import { baseURL } from "@/api";

export async function getReportsInfo(): Promise<ReportInfo[]> {
  return (await axios.get<ReportInfo[]>(baseURL + "/reports/")).data;
}
