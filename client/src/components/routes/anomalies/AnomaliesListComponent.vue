<template>
  <div class="container-lg mt-3">
    <h3>База аномалий</h3>
    <AgGridVue
      class="ag-theme-alpine"
      :column-defs="columnDefs"
      :row-data="data"
      :grid-options="options"
      @grid-ready="fitActionsColumn"
    />
  </div>
</template>

<script setup lang="ts">
import { AgGridVue } from "ag-grid-vue3";
import { ColDef, GridOptions } from "ag-grid-community";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { AnomalyInfo } from "@/types/anomalies";
import { getAnomaliesInfo } from "@/components/routes/anomalies/api";
import { dateFormatter } from "@/ag-grid/formatters";
import { routeNames } from "@/router";
import { useRouter } from "vue-router";

const router = useRouter();

const columnDefs: ColDef<AnomalyInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, minWidth: 120 },
  { headerName: "Название", field: "name", flex: 4, minWidth: 180 },
  { headerName: "Индекс", field: "anomalyIndex", flex: 4, minWidth: 180 },
  { headerName: "Площадь", field: "area", flex: 4, minWidth: 120 },
  {
    headerName: "Дата загрузки",
    field: "uploadDate",
    flex: 5,
    valueFormatter: dateFormatter,
    minWidth: 200,
  },
  {
    headerName: "Дата обнаружения",
    field: "detectDate",
    flex: 5,
    valueFormatter: dateFormatter,
    minWidth: 200,
  },
  {
    ...getActionsColDef([
      {
        tooltip: "Открыть аномалию",
        icon: "bi bi-radioactive",
        button: "btn-danger",
        onClicked: (action, data) =>
          router.push({
            name: routeNames.Anomaly,
            params: {
              id: data.id,
              name: data.name,
              anomalyIndex: data.anomalyIndex,
            },
          }),
      },
    ]),
  },
];

const options: GridOptions<AnomalyInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
};

const data = await getAnomaliesInfo();
</script>

<style scoped lang="scss"></style>
