<template>
  <div class="container-lg">
    <h2 class="text-center mt-2 text-primary">Просмотр карты №{{ id }}</h2>
    <div v-if="mapData && mapData.length" class="row justify-content-between">
      <h3 class="col">Аномалии</h3>
      <router-link
        class="col-auto"
        :to="{ name: routeNames.Report, params: { id: id } }"
      >
        <button class="btn btn-primary">Открыть отчёт</button>
      </router-link>
    </div>
    <AgGridVue
      v-if="mapData && mapData.length"
      class="ag-theme-alpine mt-3"
      :row-data="mapData"
      :column-defs="columnDefs"
      :grid-options="options"
      @grid-ready="fitActionsColumn"
    />
    <div class="d-flex justify-content-center mt-3">
      <MapDisplay :id="id" ref="mapDisplay" @map-ready="onMapReady" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { getMapData } from "@/components/routes/map/api";
import { AgGridVue } from "ag-grid-vue3";
import { ColDef, GridOptions } from "ag-grid-community";
import { AnomalyData } from "@/types/anomalies";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { routeNames } from "@/router";
import { useRouter } from "vue-router";
import L from "leaflet";

import MapDisplay from "@/components/common/map/MapDisplay.vue";

const router = useRouter();
const props = defineProps<{
  id: string;
  name?: string;
  anomalyIndex?: string;
}>();
const mapDisplay = ref<InstanceType<typeof MapDisplay>>();
let lastMarker: L.Marker | undefined = undefined;

const columnDefs: ColDef<AnomalyData>[] = [
  { headerName: "Id", field: "id", flex: 2, minWidth: 120 },
  { headerName: "Название", field: "name", flex: 4, minWidth: 180 },
  { headerName: "Площадь", field: "area", flex: 4, minWidth: 180 },
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
      {
        tooltip: "Показать на карте",
        icon: "bi bi-eye",
        button: "btn-info",
        onClicked: (action, data) => {
          if (lastMarker) {
            mapDisplay.value?.removeMarker?.(lastMarker);
          }
          lastMarker = mapDisplay.value?.addMarker?.(data.coordinates);
          mapDisplay.value?.flyToCoordinates?.(data.coordinates);
        },
      },
    ]),
  },
];

const options: GridOptions<AnomalyData> = {
  ...getDefaultGridOptions(),
  pagination: true,
  paginationPageSize: 4,
  domLayout: "autoHeight",
};

function onMapReady() {
  if (props.name && props.anomalyIndex) {
    let coordinates: [number, number] = [0, 0];
    for (let i = 0; i < mapData.length; i++) {
      if (
        mapData[i].name === props.name &&
        mapData[i].anomalyIndex == props.anomalyIndex
      ) {
        coordinates = mapData[i].coordinates;
        break;
      }
    }
    if (lastMarker) {
      mapDisplay.value?.removeMarker?.(lastMarker);
    }
    lastMarker = mapDisplay.value?.addMarker?.(coordinates);
  }
}

const mapData = await getMapData(props.id);
</script>

<style scoped lang="scss"></style>
