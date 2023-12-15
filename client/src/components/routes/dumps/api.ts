import { api } from "@/api";
import { Dump } from "@/components/routes/dumps/types";

export function downloadDump() {
  return api.get<Dump>("/dumps/");
}

export function uploadDump(file: File) {
  const formData = new FormData();
  formData.append("dump", file);
  return api.post("/dumps/", formData);
}

export const DumpsApi = { downloadDump, uploadDump };
