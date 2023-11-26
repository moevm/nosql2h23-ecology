<template>
  <div class="container-lg mt-3">
    <h3>Пользователи</h3>
    <AgGridVue
      class="ag-theme-alpine"
      :column-defs="columnDefs"
      :row-data="users"
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
import { MapInfo } from "@/types/maps";
import { onBeforeMount, ref } from "vue";
import { User } from "@/types/users";
import { UserAdminAPI } from "@/components/routes/users/api";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store/user";
import { routeNames } from "@/router";
import { ToastTypes } from "@/config/toast";
import { useToaster } from "@/store/toaster";

const router = useRouter();

const userStore = useUserStore(),
  toaster = useToaster();

const users = ref<User[]>([]);

onBeforeMount(async () => {
  users.value = (await UserAdminAPI.getUsers()).data;
});

const columnDefs: ColDef<User>[] = [
  { headerName: "Id", field: "_id.$oid", flex: 2, minWidth: 80 },
  { headerName: "Логин", field: "login", flex: 3, minWidth: 180 },
  { headerName: "Имя", field: "name", flex: 3, minWidth: 100 },
  { headerName: "Роль", field: "role", flex: 3, minWidth: 90 },

  {
    ...getActionsColDef([
      {
        tooltip: "Войти",
        icon: "bi bi-box-arrow-in-right",
        button: "btn-primary",
        onClicked: async (action, data) => {
          await userStore.login(data.login, data.password);
          await router.push({ name: routeNames.Home });
          toaster.addToast({
            title: "Выполнено",
            body: `Выполнен вход за пользователя ${data.name} (${data.login})`,
            type: ToastTypes.primary,
          });
        },
      },
      {
        tooltip: "Удалить",
        icon: "bi bi-trash",
        button: "btn-danger",
        onClicked: (action, data) => {
          /**/
        },
      },
      {
        tooltip: "Редактировать",
        icon: "bi bi-gear",
        button: "btn-warning",
        onClicked: (action, data) => {
          /**/
        },
      },
    ]),
    minWidth: 180,
  },
];

const options: GridOptions<MapInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
  animateRows: true,
};
</script>

<style scoped lang="scss"></style>
