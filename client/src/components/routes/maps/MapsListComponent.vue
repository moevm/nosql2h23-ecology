<template>
  <div class="container-lg mt-3">
    <h3>Загруженные карты</h3>
    <AgGridVue
      class="ag-theme-alpine"
      :column-defs="columnDefs"
      :grid-options="options"
      @grid-ready="onGridReady"
      @first-data-rendered="fitActionsColumn"
    />
  </div>

  <Modal ref="modal" backdrop="static">
    <template #header="{ close }">
      <h4 class="modal-title">Удалить карту</h4>
      <button type="button" class="btn-close" @click="close"></button>
    </template>

    <template #body>
      <p>Вы действительно хотите удалить карту {{ delElement }} ?</p>
    </template>

    <template #footer="{ close }">
      <button type="button" class="btn btn-secondary" @click="close">
        Отмена
      </button>
      <button type="button" class="btn btn-danger" @click="acceptDelDialog">
        Удалить
      </button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { AgGridVue } from "ag-grid-vue3";
import {
  ColDef,
  GridApi,
  GridOptions,
  GridReadyEvent,
} from "ag-grid-community";

import {
  fitActionsColumn,
  getActionsColDef,
  getGridOptionsForSSDM,
  getColDefFilterId,
  getColDefFilterText,
  getColDefFilterDate,
} from "@/ag-grid/factory";
import { DataSource } from "@/ag-grid/datasource";
import { deleteMap } from "@/components/routes/maps/api";
import { MapInfo } from "@/types/maps";
import { dateFormatter } from "@/ag-grid/formatters";
import { useRouter } from "vue-router";
import { routeNames } from "@/router";
import FlagRenderer from "@/components/renderers/FlagRenderer.vue";
import Modal from "@/components/common/Modal.vue";
import { ref } from "vue";
import { useUserStore } from "@/store/user";

const router = useRouter();
const userStore = useUserStore();
let gridApi: GridApi;

const columnDefs: ColDef<MapInfo>[] = [
  {
    headerName: "Id",
    field: "id",
    flex: 2,
    minWidth: 80,
    ...getColDefFilterId(),
  },
  {
    headerName: "Имя",
    field: "name",
    flex: 3,
    minWidth: 180,
    ...getColDefFilterText(),
  },
  {
    headerName: "Дата загрузки",
    field: "updateDatetime",
    flex: 5,
    minWidth: 180,
    valueFormatter: dateFormatter,
    ...getColDefFilterDate(),
  },
  {
    headerName: "Id загрузившего пользователя",
    field: "updateUserId",
    flex: 5,
    minWidth: 100,
    ...getColDefFilterId(),
  },
  {
    headerName: "Обработано",
    field: "ready",
    flex: 3,
    minWidth: 100,
    cellRenderer: FlagRenderer,
  },
  {
    headerName: "Нарезано",
    field: "sliced",
    flex: 3,
    minWidth: 100,
    cellRenderer: FlagRenderer,
  },
  {
    ...getActionsColDef([
      {
        tooltip: "Открыть карту",
        icon: "bi bi-map",
        button: "btn-secondary",
        hide: (data) => !(data && data.ready && data.sliced),
        onClicked: (action, data) => {
          router.push({
            name: routeNames.Map,
            params: { y: data.center[0], x: data.center[1] },
          });
        },
      },
      {
        tooltip: "Удалить карту",
        icon: "bi bi-trash",
        button: "btn-danger",
        hide: (data) =>
          !(data && data.ready && data.sliced) || !userStore.isAuthed,
        onClicked: (action, data) => {
          delElement.value = data.id;
          modal.value?.open();
        },
      },
    ]),
    minWidth: 140,
  },
];

const options: GridOptions<MapInfo> = {
  ...getGridOptionsForSSDM(),
};

function onGridReady(params: GridReadyEvent) {
  gridApi = params.api;
  gridApi.setDatasource(new DataSource("/images/table"));
}

// Для модального окна удаления.
const modal = ref<InstanceType<typeof Modal> | null>(null),
  delElement = ref<string | null>(null);

function acceptDelDialog() {
  modal.value?.close();
  if (delElement.value) deleteMap(delElement.value, gridApi);
}
</script>

<style scoped lang="scss"></style>
