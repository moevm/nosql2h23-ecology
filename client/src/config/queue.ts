export enum QueueStatus {
  processing = "processing",
  stopped = "paused",
  enqueued = "enqueued",
}

export const QueueStatusTranslation = {
  [QueueStatus.stopped]: "Остановлено",
  [QueueStatus.processing]: "Обрабатывается",
  [QueueStatus.enqueued]: "В очереди",
};
