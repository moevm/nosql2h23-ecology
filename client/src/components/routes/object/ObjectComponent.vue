<template>
  <div class="container-lg">
    <AgGridVue
      class="ag-theme-alpine mt-3"
      :column-defs="columnDefs"
      :grid-options="options"
      :row-data="[objectData]"
      style="height: 93px"
      @grid-ready="fitActionsColumn"
    />
  </div>
</template>

<script setup lang="ts">
import { ColDef, GridOptions } from "ag-grid-community";
import { ObjectData } from "@/types/objects";
import { dateFormatter } from "@/ag-grid/formatters";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { getObjectData } from "@/components/routes/object/api";
import { AgGridVue } from "ag-grid-vue3";
import { useRouter } from "vue-router";
import { routeNames } from "@/router";


const router = useRouter();
const props = defineProps<{ id: string; name: string; objectIndex: string }>();

const columnDefs: ColDef<ObjectData>[] = [
  { headerName: "Название", field: "name", flex: 4, minWidth: 180 },
  { headerName: "Индекс", field: "objectIndex", flex: 4, minWidth: 180 },
  { headerName: "Площадь", field: "area", flex: 4, minWidth: 180 },
  {
    headerName: "Дата загрузки",
    field: "uploadDate",
    flex: 5,
    minWidth: 200,
    valueFormatter: dateFormatter,
  },
  {
    headerName: "Дата обнаружения",
    field: "detectDate",
    flex: 5,
    minWidth: 200,
    valueFormatter: dateFormatter,
  },
  {
    ...getActionsColDef([
      {
        tooltip: "Показать на карте",
        icon: "bi bi-eye",
        button: "btn-info",
        onClicked: (action, data) => {
          router.push({ name: routeNames.Map, params: { id: data.id }});
        },
      },
    ]),
  },
];

const options: GridOptions<ObjectData> = {
  ...getDefaultGridOptions(),
};

const objectData = await getObjectData(
  props.id,
  props.name,
  props.objectIndex
);
</script>

<style scoped lang="scss"></style>
