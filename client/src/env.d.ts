/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly CLIENT_SERVER_URL: string;
  readonly CLIENT_MIN_ZOOM: number;
  readonly CLIENT_MAX_ZOOM: number;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
