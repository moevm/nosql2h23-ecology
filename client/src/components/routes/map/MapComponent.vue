<template>
  <div class="container-lg">
    <div class="row justify-content-between">
      <h3 class="col">Сохраненные объекты</h3>
    </div>
    <AgGridVue
      class="ag-theme-alpine mt-3"
      :row-data="objectsInfo"
      :column-defs="columnDefs"
      :grid-options="options"
      @first-data-rendered="fitActionsColumn"
    />
    <div class="d-flex justify-content-center mt-3">
      <MapDisplay :x="x" :y="y" ref="mapDisplay" @objects-updated="objectsShow"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { AgGridVue } from "ag-grid-vue3";
import { ColDef, GridOptions } from "ag-grid-community";
import { dateFormatter } from "@/ag-grid/formatters";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { routeNames } from "@/router";
import { useRouter } from "vue-router";
import L from "leaflet";

import MapDisplay from "@/components/common/map/MapDisplay.vue";
import { ObjectInfo } from "@/types/objects";


const router = useRouter();
const props = defineProps<{ x?: number; y?: number; }>();
const mapDisplay = ref<InstanceType<typeof MapDisplay>>();
let lastMarker: L.Marker | undefined = undefined;

// Надеюсь, никто не заметит этот костыль, чтобы прогружались action-ы сразу :)
const objectsInfo = ref<ObjectInfo[]>([]);

const columnDefs: ColDef<ObjectInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, minWidth: 120 },
  { headerName: "Тип", field: "type", flex: 4, minWidth: 80 },
  { headerName: "Название", field: "name", flex: 4, minWidth: 80 },
  {
    headerName: "Дата загрузки",
    field: "updateDatetime",
    flex: 5,
    minWidth: 180,
    valueFormatter: dateFormatter
  },
  {
    headerName: "Id загрузившего пользователя",
    field: "updateUserId",
    flex: 5,
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
            },
          }),
      },
      {
        tooltip: "Показать на карте",
        icon: "bi bi-eye",
        button: "btn-info",
        onClicked: (action, data) => {
          if (lastMarker) {
            mapDisplay.value?.removeMarker?.(lastMarker);
          }
          lastMarker = mapDisplay.value?.addMarker?.(data.center);
          mapDisplay.value?.flyToCoordinates?.(data.center);
        },
      },
    ]),
  }
];

const options: GridOptions<ObjectInfo> = {
  ...getDefaultGridOptions(),
  pagination: true,
  paginationPageSize: 4,
  domLayout: "autoHeight",
};

function objectsShow() {
  let objects = mapDisplay.value?.getObjects?.();
  objectsInfo.value = objects ? objects : []
}

</script>

<style scoped lang="scss"></style>
