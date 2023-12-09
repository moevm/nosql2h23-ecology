import axios, { AxiosInstance } from "axios";
import { useLoadingStore } from "@/store/loading";
import { useToaster } from "@/store/toaster";
import { ToastTypes } from "@/config/toast";

const host = import.meta.env.CLIENT_SERVER_URL ?? "localhost";
const port = import.meta.env.CLIENT_SERVER_PORT ?? "5000";

export const serverURL = `http://${host}:${port}`;
export const baseURL = `${serverURL}/api`;

export const api: AxiosInstance = axios.create({
  baseURL,
  withCredentials: true,
});

const min_map_zoom = import.meta.env.MIN_ZOOM ?? 1;
const max_map_zoom = import.meta.env.MAX_ZOOM ?? 17;

export const map_zoom = [min_map_zoom, max_map_zoom];

api.interceptors.request.use(async (req) => {
  const loadingStore = useLoadingStore();
  loadingStore.enqueue();

  return req;
});

api.interceptors.response.use(
  async (res) => {
    const loadingStore = useLoadingStore();
    loadingStore.dequeue();
    return res;
  },
  async (error) => {
    const loadingStore = useLoadingStore(),
      toaster = useToaster();

    loadingStore.dequeue();

    let data: any;
    if (error?.response?.data?.constructor === ArrayBuffer) {
      try {
        data = JSON.parse(new TextDecoder().decode(error?.response?.data));
      } catch {
        data = {};
      }
    } else {
      data = error?.response?.data;
    }

    console.error(error?.response);
    toaster.addToast({
      title: "Ошибка",
      body: data?.message ?? data ?? "Ошибка сервера",
      type: ToastTypes.danger,
    });

    throw error;
  }
);

export const objectTypesColors: Map<string, string> = new Map();
objectTypesColors.set("Лес", "green");
objectTypesColors.set("Вырубка", "red");
objectTypesColors.set("Поляна", "aquamarine");
objectTypesColors.set("Дом", "darkgrey");
