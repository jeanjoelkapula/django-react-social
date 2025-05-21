const initialState = {
    id: 0,
    isSelected: false,
    participants:[],
    chat_messages:[],
    chat: {
        id:0
    }
};
const SET_CURRENT_CHAT = "SET_CURRENT_CHAT";
const ADD_CURRENT_CHAT_MESSAGE = "ADD_CURRENT_CHAT_MESSAGE";

export function setCurrentChat(payload) {
    return {
        type: SET_CURRENT_CHAT,
        payload
    }
}

export function addCurrentChatMessage(payload) {
    return {
        type: ADD_CURRENT_CHAT_MESSAGE,
        payload
    }
}

export default function currentChatReducer(state = initialState, action) {
    switch(action.type) {
        case SET_CURRENT_CHAT:
            return action.payload
        case ADD_CURRENT_CHAT_MESSAGE:
            return {
                ...state,
                chat_messages:[
                    ...state.chat_messages,
                    action.payload
                ]
            }
        default:
            return state;
    }
}