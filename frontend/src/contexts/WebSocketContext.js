import { createContext } from "react";
const WebSocketContext = createContext(null);
export const WebSocketProvider = WebSocketContext.Provider;
export default WebSocketContext;