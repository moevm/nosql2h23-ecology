import { ref, readonly } from "vue";
import { MapInfo } from "@/types/maps";
import { getMapsInfo } from "@/components/routes/maps/api";
import { socket } from "@/api/websocket/index";
import {
  createSharedComposable,
  tryOnBeforeMount,
  tryOnScopeDispose,
} from "@vueuse/core";

export const useImages = createSharedComposable(async () => {
  const images = ref<MapInfo[]>([]);
  tryOnBeforeMount(() =>
    socket.on("images", (newImages: MapInfo[]) => (images.value = newImages))
  );
  tryOnScopeDispose(() => socket.off("queue"));
  images.value = await getMapsInfo();
  return { images: readonly(images) };
});
