<template>
  <div class="container-lg mt-3">
    <h3>Загруженные карты</h3>
    <AgGridVue
      class="ag-theme-alpine"
      :column-defs="columnDefs"
      :row-data="images"
      :grid-options="options"
      @grid-ready="fitActionsColumn"
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
import { ColDef, GridOptions } from "ag-grid-community";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { deleteMap } from "@/components/routes/maps/api";
import { MapInfo } from "@/types/maps";
import { dateFormatter } from "@/ag-grid/formatters";
import { useRouter } from "vue-router";
import { routeNames } from "@/router";
import FlagRenderer from "@/components/renderers/FlagRenderer.vue";
import Modal from "@/components/common/Modal.vue";
import { useImages } from "@/api/websocket/images";
import { ref } from "vue";

const router = useRouter();

const columnDefs: ColDef<MapInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, minWidth: 80 },
  { headerName: "Имя", field: "name", flex: 3, minWidth: 180 },
  {
    headerName: "Дата загрузки",
    field: "date",
    flex: 5,
    minWidth: 180,
    valueFormatter: dateFormatter,
  },
  {
    headerName: "Размер",
    field: "size",
    flex: 5,
    minWidth: 180,
    valueFormatter: ({ value }: { value: number }) =>
      `${Math.round(value / 1048576)} Мб`,
  },
  {
    headerName: "Обработано",
    field: "ready",
    flex: 3,
    minWidth: 200,
    cellRenderer: FlagRenderer,
  },
  {
    headerName: "Нарезано",
    field: "sliced",
    flex: 3,
    minWidth: 200,
    cellRenderer: FlagRenderer,
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
      {
        tooltip: "Открыть отчёт",
        icon: "bi bi-file-text",
        button: "btn-primary",
        hide: (data) => !data.ready,
        onClicked: (action, data) =>
          router.push({ name: routeNames.Report, params: { id: data.id } }),
      },
      {
        tooltip: "Удалить карту",
        icon: "bi bi-trash",
        button: "btn-danger",
        hide: (data) => !(data.ready && data.sliced),
        onClicked: (action, data) => {
          delElement.value = data.id;
          modal.value?.open();
        },
      },
    ]),
  },
];

const options: GridOptions<MapInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
  animateRows: true,
};

const { images } = await useImages();

// Для модального окна удаления.
const modal = ref<InstanceType<typeof Modal> | null>(null),
  delElement = ref<string | null>(null);

function acceptDelDialog() {
  modal.value?.close();
  if (delElement.value) deleteMap(delElement.value);
}
</script>

<style scoped lang="scss"></style>
