/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly CLIENT_SERVER_URL: string;
  readonly CLIENT_SERVER_PORT: string;
  readonly MIN_ZOOM: number;
  readonly MAX_ZOOM: number;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
