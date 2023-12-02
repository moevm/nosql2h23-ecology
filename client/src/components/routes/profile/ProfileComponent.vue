<template>
  <div class="container-lg mt-3">
    <div class="row justify-content-center">
      <i
        class="col-auto text-primary bi bi-person-circle"
        style="font-size: 256px"
      />
      <div class="col-auto">
        <div class="fs-4 d-flex align-items-center">
          <span class="fs-3">{{ userStore.user?.login }}</span>
          <span class="badge bg-secondary ms-3">
            #{{ userStore.user?._id.$oid }}
          </span>
          <i
            class="bi bi-person-gear fs-1 text-primary ms-5"
            role="button"
            @click="edit"
          />
        </div>
        <div class="fs-4 mt-2">
          <div>Имя: {{ userStore.user?.name }}</div>
          <div class="mt-1">
            Роль:
            {{ UserRoleTranslations[userStore.user?.role ?? UserRole.user] }}
          </div>
        </div>
      </div>
    </div>

    <EditProfileModal
      v-if="userStore.user"
      ref="editUserModal"
      :user="userStore.user"
      @submit="onEdit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useUserStore } from "@/store/user";
import { useToaster } from "@/store/toaster";
import { UserRole, UserRoleTranslations } from "@/config/users";
import EditProfileModal from "@/components/routes/profile/EditProfileModal.vue";
import { User } from "@/types/users";
import _ from "lodash";
import { ProfileAPI } from "@/components/routes/profile/api";
import { ToastTypes } from "@/config/toast";

const editUserModal = ref<InstanceType<typeof EditProfileModal> | null>(null);

const userStore = useUserStore(),
  toaster = useToaster();

function edit() {
  editUserModal.value?.modal?.open();
}

async function onEdit(data: User) {
  await ProfileAPI.updateSelf(_.pick(data, ["login", "name", "password"]));
  await userStore.fetchUser();
  toaster.addToast({
    title: "Обновлено",
    body: "Профиль успешно обновлён",
    type: ToastTypes.success,
  });
}
</script>

<style scoped lang="scss"></style>
