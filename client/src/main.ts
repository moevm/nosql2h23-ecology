import { createApp } from "vue";
import { router } from "@/router";
import App from "@/App.vue";
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { vBsTooltip } from "@/bootstrap/tooltip";
import { plugin, defaultConfig } from "@formkit/vue";
import "@formkit/themes/genesis";
import { createPinia } from "pinia";
import { useUserStore } from "@/store/user";

async function bootstrap() {
  const pinia = createPinia();

  const userStore = useUserStore(pinia);
  await userStore.fetchUser();

  const app = createApp(App);
  app.use(router);
  app.use(plugin, defaultConfig());
  app.use(pinia);
  app.directive("bs-tooltip", vBsTooltip);
  app.mount("#app");
}

bootstrap();
