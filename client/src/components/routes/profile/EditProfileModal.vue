<template>
  <Modal ref="modal" backdrop="static" @opened="onOpened">
    <template #header="{ close }">
      <h4 class="modal-title">Редактировать данные</h4>
      <button type="button" class="btn-close" @click="close"></button>
    </template>

    <template v-if="user" #body>
      <FormKit v-model="user" type="form" :actions="false">
        <FormKit name="login" type="text" label="Логин" />
        <FormKit name="name" type="text" label="Имя" />
        <FormKit name="password" type="text" label="Пароль" />
      </FormKit>
    </template>

    <template #footer="{ close }">
      <button type="button" class="btn btn-secondary" @click="close">
        Отмена
      </button>
      <button type="button" class="btn btn-danger" @click="submit">
        Подтвердить
      </button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from "@/components/common/Modal.vue";
import { ref } from "vue";
import { User } from "@/types/users";
import _ from "lodash";

const props = defineProps<{ user: User }>();

const emit = defineEmits<{ (e: "submit", u: User): void }>();

const modal = ref<InstanceType<typeof Modal> | null>(null);

const user = ref<User | null>(null);

function onOpened() {
  user.value = _.cloneDeep(props.user);
}

function submit() {
  if (user.value) {
    emit("submit", user.value);
  }

  modal.value?.close();
}

defineExpose({ modal });
</script>

<style scoped lang="scss"></style>
