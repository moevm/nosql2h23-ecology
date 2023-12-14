<template>
  <div class="container-lg mt-3">
    <h3 class="d-flex justify-content-between">
      Пользователи
      <button class="btn btn-primary" @click="showAddModal">
        Добавить
        <i class="bi bi-plus-circle"></i>
      </button>
    </h3>
    <AgGridVue
      class="ag-theme-alpine"
      :column-defs="columnDefs"
      :row-data="users"
      :grid-options="options"
      @grid-ready="onGridReady"
    />

    <UserDataModal
      v-if="selected"
      ref="addUserModal"
      :user="selected"
      @submit="onAdd"
    />

    <UserDataModal
      v-if="selected"
      ref="editUserModal"
      :user="selected"
      @submit="onEdit"
    />

    <Modal ref="deleteModal" backdrop="static">
      <template #header="{ close }">
        <h4 class="modal-title">Удалить пользователя</h4>
        <button type="button" class="btn-close" @click="close"></button>
      </template>

      <template #body>
        <p>
          Вы действительно хотите удалить пользователя {{ selected?.name }} ({{
            selected?.login
          }}) ?
        </p>
      </template>

      <template #footer="{ close }">
        <button type="button" class="btn btn-secondary" @click="close">
          Отмена
        </button>
        <button type="button" class="btn btn-danger" @click="onRemove">
          Удалить
        </button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { AgGridVue } from "ag-grid-vue3";
import { nextTick, ref } from "vue";
import _ from "lodash";
import { ColDef, GridOptions, GridReadyEvent } from "ag-grid-community";

import {
  fitActionsColumn,
  getActionsColDef,
  getGridOptionsForSSDM,
  getColDefFilterText
} from "@/ag-grid/factory";
import { DataSource } from "@/ag-grid/datasource";
import { User } from "@/types/users";
import { UserAdminAPI } from "@/components/routes/users/api";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store/user";
import { routeNames } from "@/router";
import { ToastTypes } from "@/config/toast";
import { useToaster } from "@/store/toaster";
import UserDataModal from "@/components/routes/users/UserDataModal.vue";
import Modal from "@/components/common/Modal.vue";
import { getEmptyUser } from "@/config/users";


const router = useRouter();

const editUserModal = ref<InstanceType<typeof UserDataModal> | null>(null),
  addUserModal = ref<InstanceType<typeof UserDataModal> | null>(null),
  deleteModal = ref<InstanceType<typeof Modal> | null>(null);

const userStore = useUserStore(),
  toaster = useToaster();

const users = ref<User[]>([]),
  selected = ref<User | null>(null);

const columnDefs: ColDef<User>[] = [
  { headerName: "Id", field: "_id.$oid", flex: 2, minWidth: 80, ...getColDefFilterText() },
  { headerName: "Логин", field: "login", flex: 3, minWidth: 180, ...getColDefFilterText() },
  { headerName: "Имя", field: "name", flex: 3, minWidth: 100, ...getColDefFilterText() },
  { headerName: "Роль", field: "role", flex: 3, minWidth: 90, ...getColDefFilterText() },

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
          selected.value = data;
          nextTick(() => deleteModal.value?.open());
        },
      },
      {
        tooltip: "Редактировать",
        icon: "bi bi-gear",
        button: "btn-warning",
        onClicked: (action, data) => {
          selected.value = data;
          nextTick(() => editUserModal.value?.modal?.open());
        },
      },
    ]),
    minWidth: 180,
  },
];

const options: GridOptions = {
  ...getGridOptionsForSSDM(),
  domLayout: "autoHeight",
  animateRows: true,
};

function onGridReady(params: GridReadyEvent) {
  fitActionsColumn({ "columnApi": params.columnApi });
  params.api.setDatasource(new DataSource("/users/table"));
}

function showAddModal() {
  selected.value = getEmptyUser();
  nextTick(() => addUserModal.value?.modal?.open());
}

async function onAdd(user: User) {
  const id = (await UserAdminAPI.createUser(_.omit(user, "_id"))).data;
  users.value = [{ ...user, _id: { $oid: id } }, ...users.value];
}

async function onRemove() {
  if (selected.value) {
    await UserAdminAPI.deleteUser(selected.value._id.$oid);
    users.value = users.value.filter(
      (u) => u._id.$oid !== selected.value?._id.$oid
    );
    deleteModal.value?.close();
  }
}

async function onEdit(user: User) {
  await UserAdminAPI.updateUser(user._id.$oid, _.omit(user, "_id"));
  _.assign(selected.value, user);
  options.api?.refreshCells();
}
</script>

<style scoped lang="scss"></style>
