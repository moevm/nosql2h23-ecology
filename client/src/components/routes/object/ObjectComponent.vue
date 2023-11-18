<template>
  <div class="container-lg">
    <h2 class="text-center mt-2 text-primary">
      Просмотр объекты {{ name }} номер {{ objectIndex }} на карте №{{ id }}
    </h2>
    <div class="row justify-content-end">
    </div>

    <AgGridVue
      class="ag-theme-alpine mt-3"
      :column-defs="columnDefs"
      :grid-options="options"
      :row-data="[objectData]"
      style="height: 93px"
      @grid-ready="fitActionsColumn"
    />

    <div class="d-flex justify-content-center mt-3">
      <MapDisplay :id="id" ref="mapDisplay" @map-ready="onMapReady" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ColDef, GridOptions } from "ag-grid-community";
import { ObjectData } from "@/types/objects";
import { dateFormatter } from "@/ag-grid/formatters";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { routeNames } from "@/router";
import { getObjectData } from "@/components/routes/object/api";
import { AgGridVue } from "ag-grid-vue3";
import MapDisplay from "@/components/common/map/MapDisplay.vue";

const props = defineProps<{ id: string; name: string; objectIndex: string }>();
const mapDisplay = ref<InstanceType<typeof MapDisplay>>();

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
          mapDisplay.value?.flyToCoordinates?.(objectData.coordinates);
        },
      },
    ]),
  },
];

const options: GridOptions<ObjectData> = {
  ...getDefaultGridOptions(),
};

function onMapReady() {
  mapDisplay.value?.addMarker?.(objectData.coordinates);
}

const objectData = await getObjectData(
  props.id,
  props.name,
  props.objectIndex
);
</script>

<style scoped lang="scss"></style>
