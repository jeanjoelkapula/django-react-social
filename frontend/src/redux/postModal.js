const initialState = false;
const SET_SHOWN = "SET_SHOWN";

export function setModalShown(payload) {
    return {
        type: SET_SHOWN,
        payload
    }
}

export default function PostModalReducer(state = initialState, action) {
    switch(action.type) {
        case SET_SHOWN:
            return action.payload;
        default:
            return state;
    }
}