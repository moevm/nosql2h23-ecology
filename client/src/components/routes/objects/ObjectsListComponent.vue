<template>
  <div class="container-lg mt-3">
    <h3>База объектов</h3>
    <div class="text-end mb-2">
      <button class="btn btn-primary" @click="exportData">Экспорт</button>
    </div>
    <AgGridVue
      class="ag-theme-alpine"
      :column-defs="columnDefs"
      :grid-options="options"
      @grid-ready="onGridReady"
      @first-data-rendered="fitActionsColumn"
    />
  </div>
</template>

<script setup lang="ts">
import { AgGridVue } from "ag-grid-vue3";
import { ColDef, GridOptions, GridReadyEvent } from "ag-grid-community";
import { useRouter } from "vue-router";
import { saveAs } from "file-saver";

import {
  fitActionsColumn,
  getActionsColDef,
  getGridOptionsForSSDM,
  getColDefFilterId,
  getColDefFilterText,
  getColDefFilterDate
} from "@/ag-grid/factory";
import { DataSource } from "@/ag-grid/datasource";
import { dateFormatter } from "@/ag-grid/formatters";
import { routeNames } from "@/router";
import { ObjectInfo } from "@/types/objects";
import { exportObjects } from "@/components/routes/objects/api";


const router = useRouter();

const columnDefs: ColDef<ObjectInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, minWidth: 120, ...getColDefFilterId() },
  { headerName: "Тип", field: "type", flex: 4, minWidth: 80, ...getColDefFilterText() },
  { headerName: "Название", field: "name", flex: 4, minWidth: 80, ...getColDefFilterText() },
  {
    headerName: "Дата изменения",
    field: "updateDatetime",
    flex: 5,
    minWidth: 200,
    valueFormatter: dateFormatter,
    ...getColDefFilterDate()
  },
  {
    headerName: "Id изменившего пользователя",
    field: "updateUserId",
    flex: 5,
    minWidth: 100,
    ...getColDefFilterId()
  },
  {
    ...getActionsColDef([
      {
        tooltip: "Открыть объект",
        icon: "bi bi-radioactive",
        button: "btn-danger",
        onClicked: (action, data) =>
          router.push({
            name: routeNames.Object,
            params: { id: data.id },
          }),
      },
    ]),
  },
];

const options: GridOptions<ObjectInfo> = {
  ...getGridOptionsForSSDM(),
  domLayout: "autoHeight",
};

function onGridReady(params: GridReadyEvent) {
  params.api.setDatasource(new DataSource("/objects/table"));
}

async function exportData() {
  const data = (await exportObjects()).data;
  const blob = new Blob([JSON.stringify(data)], {
    type: "text/plain;charset=utf-8",
  });
  saveAs(blob, "objects.json");
}
</script>

<style scoped lang="scss"></style>
