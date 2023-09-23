<template>
  <div class="container-lg mt-3">
    <h3>Очередь обработки</h3>
    <AgGridVue
      class="ag-theme-alpine"
      :column-defs="columnDefs"
      :row-data="queue"
      :grid-options="options"
      :get-row-id="getRowId"
      @grid-ready="fitActionsColumn"
      @row-data-updated="onRowDataUpdated"
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
import { QueueItemInfo } from "@/types/queue";
import { dateFormatter } from "@/ag-grid/formatters";
import { useRouter } from "vue-router";
import ProgressRenderer from "@/components/routes/queue/components/ProgressRenderer.vue";
import { useQueue } from "@/api/websocket/queue";
import { routeNames } from "@/router";
import StatusRenderer from "@/components/routes/queue/components/StatusRenderer.vue";

const router = useRouter();

const columnDefs: ColDef<QueueItemInfo>[] = [
  { headerName: "Id", field: "id", flex: 3, minWidth: 240 },
  { headerName: "Название", field: "name", flex: 2, minWidth: 180 },
  {
    headerName: "Дата загрузки",
    field: "uploadDate",
    flex: 2,
    valueFormatter: dateFormatter,
    minWidth: 200,
  },
  {
    headerName: "Прогресс",
    field: "progress",
    flex: 2,
    cellRenderer: ProgressRenderer,
    cellClass: "row d-flex align-items-center",
    minWidth: 180,
  },
  {
    headerName: "Статус",
    field: "status",
    flex: 2,
    cellRenderer: StatusRenderer,
    cellClass: "row d-flex align-items-center",
    minWidth: 180,
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
    ]),
  },
];

const options: GridOptions<QueueItemInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
  rowDragManaged: true,
  animateRows: true,
};

function onRowDataUpdated() {
  options.columnApi?.autoSizeColumn?.("actions", true);
}

function getRowId({ data }: { data: QueueItemInfo }) {
  return data.id;
}

const { queue } = useQueue();
</script>

<style scoped lang="scss"></style>
