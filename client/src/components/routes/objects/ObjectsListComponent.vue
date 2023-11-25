<template>
  <div class="container-lg mt-3">
    <h3>База объектов</h3>
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
import { ObjectInfo } from "@/types/objects";
import { getObjectsInfo } from "@/components/routes/objects/api";
import { dateFormatter } from "@/ag-grid/formatters";
import { routeNames } from "@/router";
import { useRouter } from "vue-router";

const router = useRouter();

const columnDefs: ColDef<ObjectInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, minWidth: 120 },
  { headerName: "Название", field: "name", flex: 4, minWidth: 180 },
  { headerName: "Индекс", field: "objectIndex", flex: 4, minWidth: 180 },
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
        tooltip: "Открыть объект",
        icon: "bi bi-radioactive",
        button: "btn-danger",
        onClicked: (action, data) =>
          router.push({
            name: routeNames.Object,
            params: {
              id: data.id,
              name: data.name,
              objectIndex: data.objectIndex,
            },
          }),
      },
    ]),
  },
];

const options: GridOptions<ObjectInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
};

const data = await getObjectsInfo();
</script>

<style scoped lang="scss"></style>
