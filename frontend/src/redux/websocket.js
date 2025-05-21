import { WEBSOCKET_BASE } from "../URL_config";

const CONNECT = "CONNECT";
const DISCONNECT = "DISCONNECT";
const SET_SOCKET = "SET_CONNECT";

export function setSocket(payload) {
    return {
        type: SET_SOCKET,
        payload
    }
}

export function connect(payload) {
    const {auth} = payload;

    return (dispatch)=> {
        const socket_url = WEBSOCKET_BASE + auth.user.username + "/?token=" + auth.token;
        const websocket = new WebSocket(socket_url);

        dispatch(setSocket(websocket));
    }
}

export default function webSocketReducer(state = null, action) {
    switch(action.type) {
        case SET_SOCKET:
            return action.payload;
        case CONNECT:
            return action.payload;
        case DISCONNECT:
            return null;
        default:
            return state;
    }
}