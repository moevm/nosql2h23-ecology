/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly CLIENT_SERVER_URL: string;
  readonly CLIENT_SERVER_PORT: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
