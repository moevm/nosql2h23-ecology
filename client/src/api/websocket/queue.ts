import { ref, readonly } from "vue";
import { QueueItemInfo } from "@/types/queue";
import { socket } from "@/api/websocket/index";
import {
  createSharedComposable,
  tryOnBeforeMount,
  tryOnScopeDispose,
} from "@vueuse/core";

export const useQueue = createSharedComposable(() => {
  const queue = ref<QueueItemInfo[]>([]);
  tryOnBeforeMount(() =>
    socket.on("queue", (newQueue: QueueItemInfo[]) => (queue.value = newQueue))
  );
  tryOnScopeDispose(() => socket.off("queue"));
  return { queue: readonly(queue) };
});
