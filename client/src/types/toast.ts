import { ToastTypes } from "@/config/toast";

export interface ToastData {
  id: number;
  type?: ToastTypes;
  title?: string;
  body?: string;
  time?: number;
}
