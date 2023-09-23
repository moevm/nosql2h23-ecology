import { io } from "socket.io-client";
import { serverURL } from "@/api";

export const socket = io(serverURL);
