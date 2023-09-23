import { QueueStatus } from "@/config/queue";

export interface QueueItemInfo {
  id: string;
  name: string;
  uploadDate: string;
  progress: number;
  status: QueueStatus;
}
