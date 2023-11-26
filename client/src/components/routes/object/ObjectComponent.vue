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
import { ObjectInfo } from "@/types/objects";
import { dateFormatter } from "@/ag-grid/formatters";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { getObjectsInfo } from "@/components/routes/object/api";
import { AgGridVue } from "ag-grid-vue3";
import { useRouter } from "vue-router";
import { routeNames } from "@/router";


const router = useRouter();
const props = defineProps<{ id: string }>();

const columnDefs: ColDef<ObjectInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, minWidth: 120 },
  { headerName: "Тип", field: "type", flex: 4, minWidth: 80 },
  { headerName: "Название", field: "name", flex: 4, minWidth: 80 },
  {
    headerName: "Дата загрузки",
    field: "updateDatetime",
    flex: 5,
    minWidth: 180,
    valueFormatter: dateFormatter,
  },
  {
    headerName: "Id загрузившего пользователя",
    field: "updateUserId",
    flex: 5,
    minWidth: 100,
  },
  {
    ...getActionsColDef([
      {
        tooltip: "Показать на карте",
        icon: "bi bi-eye",
        button: "btn-info",
        onClicked: (action, data) => {
          router.push({ name: routeNames.Map, params: { 
            y: data.center[0],
            x: data.center[1]}
          });
        },
      },
    ]),
  },
];

const options: GridOptions<ObjectInfo> = {
  ...getDefaultGridOptions(),
};

const objectData = await getObjectsInfo(props.id);
</script>

<style scoped lang="scss"></style>
