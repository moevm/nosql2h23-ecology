import axios, { AxiosInstance } from "axios";

const host = import.meta.env.CLIENT_SERVER_URL ?? "localhost";
const port = import.meta.env.CLIENT_SERVER_PORT ?? "5000";

export const serverURL = `http://${host}:${port}`;
export const baseURL = `${serverURL}/api`;

export const api: AxiosInstance = axios.create({
  baseURL,
  withCredentials: true,
});

const min_map_zoom = import.meta.env.MIN_ZOOM ?? 1;
const max_map_zoom = import.meta.env.MAX_ZOOM ?? 15;

export const map_zoom = [min_map_zoom, max_map_zoom];
