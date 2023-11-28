<template>
  <div class="container">
    <div class="card col-12 col-md-6 m-auto mt-2">
      <div class="card-body m-auto">
        <h1 class="text-center">Войти</h1>
        <FormKit v-model="login" type="text" label="Логин" />
        <FormKit v-model="password" type="password" label="Пароль" />

        <div class="text-end">
          <button class="btn btn-primary" @click="doLogin">Войти</button>
        </div>

        <div class="text-end mt-3">
          <div class="alert alert-danger">
            <button class="d-block w-100 btn btn-danger me-2" @click="devLogin">
              Войти dev
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useUserStore } from "@/store/user";
import { useToaster } from "@/store/toaster";
import { ToastTypes } from "@/config/toast";
import { useRouter } from "vue-router";
import { routeNames } from "@/router";

const router = useRouter();

const userStore = useUserStore(),
  toaster = useToaster();

const login = ref(""),
  password = ref("");

async function doLogin() {
  try {
    await userStore.login(login.value, login.password);
    toaster.addToast({
      title: "Выполнено",
      body: "Вы вошли в аккаунт",
      type: ToastTypes.primary,
    });
    router.push({ name: routeNames.Home });
  }
  catch (err) {
    toaster.addToast({
      title: "Ошибка",
      body: "Неверные данные",
      type: ToastTypes.danger,
    });
  }

}

async function devLogin() {
  await userStore.devLogin();
  toaster.addToast({
    title: "Выполнено",
    body: "Выполнен вход для разработчика",
    type: ToastTypes.primary,
  });

  router.push({ name: routeNames.Home });
}
</script>
