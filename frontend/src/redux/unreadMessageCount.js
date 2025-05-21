const initialState = "";
const SET_MESSAGE_COUNT = "SET_MESSAGE_COUNT";

export function setMessageCount(payload) {
    return {
        type: SET_MESSAGE_COUNT,
        payload
    }
}

export default function messageCountReducer(state = initialState, action) {
    switch(action.type) {
        case SET_MESSAGE_COUNT:
            let value = "";
            if (action.payload > 0) {
                value = action.payload;
            }
            return value;
        
        default:
            return state;
    }
}