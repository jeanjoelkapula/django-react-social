export const API_BASE_URL = 'http://127.0.0.1:8000/api';
const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
export const WEBSOCKET_BASE = 
                'ws://127.0.0.1:8000/'
                + 'ws/chat/';
 