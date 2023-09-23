<template>
  <div class="container-lg mt-3">
    <h3>Отчёты обработанных карт</h3>
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
import { getReportsInfo } from "@/components/routes/reports/api";
import { ReportInfo } from "@/types/reports";
import { dateFormatter } from "@/ag-grid/formatters";
import { routeNames } from "@/router";
import { useRouter } from "vue-router";

const router = useRouter();

const columnDefs: ColDef<ReportInfo>[] = [
  { headerName: "Id изображения", field: "id", flex: 2, minWidth: 120 },
  { headerName: "Имя изображения", field: "name", flex: 3, minWidth: 180 },
  {
    headerName: "Дата загрузки",
    field: "date",
    flex: 5,
    valueFormatter: dateFormatter,
    minWidth: 200,
  },
  {
    headerName: "Количество аномалий",
    field: "anomalies",
    flex: 2,
    minWidth: 120,
  },
  {
    ...getActionsColDef([
      {
        tooltip: "Открыть карту",
        icon: "bi bi-map",
        button: "btn-secondary",
        onClicked: (action, data) =>
          router.push({ name: routeNames.Map, params: { id: data.id } }),
      },
      {
        tooltip: "Открыть отчёт",
        icon: "bi bi-file-text",
        button: "btn-primary",
        onClicked: (action, data) =>
          router.push({ name: routeNames.Report, params: { id: data.id } }),
      },
    ]),
  },
];

const options: GridOptions<ReportInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
};

const data = await getReportsInfo();
</script>

<style scoped lang="scss"></style>
