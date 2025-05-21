const initialState = [];

const SET_CHATS = "SET_CHATS";
const ADD_CHAT = "ADD_CHAT";
const SET_SELECTED = "SET_SELECTED";
const ADD_MESSAGE = "ADD_MESSAGE";
const UPDATE_MESSAGES_READ_STATUS = "UPDATE_MESSAGES_READ_STATUS";

export function setChats(payload) {
    return {
        type: SET_CHATS,
        payload
    }
}

export function addChat(payload) {
    return {
        type: ADD_CHAT,
        payload
    }
}

export function addMessage(payload) {
    return {
        type: ADD_MESSAGE,
        payload
    }
}

export function updateMessagesReadStatus(payload) {
    return {
        type: UPDATE_MESSAGES_READ_STATUS,
        payload
    }
}

export function setSelected(payload) {
    return {
        type: SET_SELECTED,
        payload
    }
}

export default function chatsReducer(state = initialState, action) {
    switch(action.type) {
        case SET_CHATS:
            return action.payload;
        case ADD_CHAT:
            return [
                action.payload,
                ...state
            ]
        case ADD_MESSAGE:
            const new_chats = state.map(chat=>{
                if (chat.id === action.payload.chat) {
                    return {
                        ...chat,
                        chat_messages:[
                            ...chat.chat_messages,
                            action.payload.message
                        ],
                        unread_count:action.payload.total_unread_count
                    }
                }
                else {
                    return {
                        ...chat
                    }
                }
            });

            return new_chats;
        
        case UPDATE_MESSAGES_READ_STATUS:
            const chats = state.map(chat => {
                if (chat.id === action.payload.chat) {
                    const chat_messages = chat.chat_messages.map(message => {
                        if (message.read) {
                            return {...message}
                        }
                        else {
                            return {
                                ...message,
                                read: true
                            }
                        }
                    });

                    return {
                        ...chat,
                        chat_messages,
                        unread_count: 0
                    }
                }
                else {
                    return {...chat}
                }
            });  

            return chats;

        case SET_SELECTED:
            return {
                ...state,
                isSelected:action.payload
            }
        default:
            return state
    }
}