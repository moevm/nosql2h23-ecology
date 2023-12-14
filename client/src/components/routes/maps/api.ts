import { api } from "@/api";
import { GridApi } from "ag-grid-community";


export function deleteMap(id: string, gridApi: GridApi) {
  return api.delete("/images/image/" + id
  ).then(() => {
    gridApi.refreshInfiniteCache();
  });
}
