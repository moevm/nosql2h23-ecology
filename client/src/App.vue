<template>
  <nav class="navbar navbar-expand-lg bg-light">
    <div class="container-fluid px-3">
      <router-link :to="{ name: routeNames.MapsList }" class="navbar-brand">
        <i class="bi bi-map fs-2" />
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div id="navbar" class="collapse navbar-collapse fs-6">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li v-for="route of routes" :key="route" class="nav-item ps-4">
            <router-link
              :to="{ name: route }"
              class="nav-link"
              active-class="active"
            >
              {{ routesTranslation[route] }}
            </router-link>
          </li>
          <li class="nav-item ps-4">
            <router-link
              :to="{ name: routeNames.Home }"
              class="nav-link"
              active-class="text-info"
            >
              О проекте
            </router-link>
          </li>

          <li v-if="userStore.role === UserRole.admin" class="nav-item ps-4">
            <router-link
              :to="{ name: routeNames.Users }"
              class="nav-link text-warning"
              active-class="text-info"
            >
              Пользователи
            </router-link>
          </li>
        </ul>
      </div>
      <div class="fs-2 text-primary" role="button">
        <i
          v-if="userStore.isAuthed"
          class="bi bi-box-arrow-left"
          @click="logout"
        />
        <router-link
          v-else
          :to="{ name: routeNames.Auth }"
          class="nav-link"
          active-class="text-info"
        >
          <i class="bi bi-box-arrow-in-right" />
        </router-link>
      </div>
    </div>
  </nav>
  <main>
    <router-view />
    <LoadingBottomCard
      v-if="loadingStore.showProgress"
      :processed="loadingStore.processed"
      :enqueued="loadingStore.enqueued"
    />
  </main>
  <ToasterComponent />
</template>

<script setup lang="ts">
import { routeNames } from "@/router";
import ToasterComponent from "@/components/common/ToasterComponent.vue";
import { useUserStore } from "@/store/user";
import { useToaster } from "@/store/toaster";
import { ToastTypes } from "@/config/toast";
import { UserRole } from "@/config/users";
import { computed } from "vue";
import LoadingBottomCard from "@/components/common/LoadingBottomCard.vue";
import { useLoadingStore } from "@/store/loading";

const userStore = useUserStore(),
  toaster = useToaster(),
  loadingStore = useLoadingStore();

const routes = computed(() => [
  routeNames.Map,
  routeNames.MapsList,
  routeNames.Queue,
  routeNames.ObjectsList,
  ...(userStore.isAuthed ? [routeNames.Upload, routeNames.Profile] : []),
]);
const routesTranslation = {
  [routeNames.Map]: "Глобальная карта",
  [routeNames.MapsList]: "Карты",
  [routeNames.Queue]: "Очередь",
  [routeNames.ObjectsList]: "Объекты",
  [routeNames.Upload]: "Загрузить",
  [routeNames.Profile]: "Профиль",
};

async function logout() {
  await userStore.logout();
  toaster.addToast({
    title: "Выполнено",
    body: "Вы вышли из аккаунта",
    type: ToastTypes.info,
  });
}
</script>

<style lang="scss">
@import "@/scss/app.scss";
</style>
