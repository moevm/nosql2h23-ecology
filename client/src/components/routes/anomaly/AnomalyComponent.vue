<template>
  <div class="container-lg">
    <h2 class="text-center mt-2 text-primary">
      Просмотр аномалии {{ name }} номер {{ anomalyIndex }} на карте №{{ id }}
    </h2>
    <div class="row justify-content-end">
      <router-link
        class="col-auto"
        :to="{ name: routeNames.Report, params: { id: anomalyData.id } }"
      >
        <button class="btn btn-primary">Открыть отчёт</button>
      </router-link>
    </div>

    <AgGridVue
      class="ag-theme-alpine mt-3"
      :column-defs="columnDefs"
      :grid-options="options"
      :row-data="[anomalyData]"
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
import { AnomalyData } from "@/types/anomalies";
import { dateFormatter } from "@/ag-grid/formatters";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { routeNames } from "@/router";
import { getAnomalyData } from "@/components/routes/anomaly/api";
import { AgGridVue } from "ag-grid-vue3";
import MapDisplay from "@/components/common/map/MapDisplay.vue";

const props = defineProps<{ id: string; name: string; anomalyIndex: string }>();
const mapDisplay = ref<InstanceType<typeof MapDisplay>>();

const columnDefs: ColDef<AnomalyData>[] = [
  { headerName: "Название", field: "name", flex: 4, minWidth: 180 },
  { headerName: "Индекс", field: "anomalyIndex", flex: 4, minWidth: 180 },
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
          mapDisplay.value?.flyToCoordinates?.(anomalyData.coordinates);
        },
      },
    ]),
  },
];

const options: GridOptions<AnomalyData> = {
  ...getDefaultGridOptions(),
};

function onMapReady() {
  mapDisplay.value?.addMarker?.(anomalyData.coordinates);
}

const anomalyData = await getAnomalyData(
  props.id,
  props.name,
  props.anomalyIndex
);
</script>

<style scoped lang="scss"></style>
