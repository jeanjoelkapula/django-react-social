const initialState = {
    isLoading: false,
    message: null
}

const SET_LOADING = "SET_LOADING";
const SET_MESSAGE = "SET_MESSAGE";

export function setAuthLoading(payload) {
    return {
        type: SET_LOADING,
        payload: payload
    }
}

export function setAuthMessage(payload) {
    return {
        type: SET_MESSAGE,
        payload: payload
    }
}

export default function authReducer(state = initialState, action) {
    switch(action.type) {
        case SET_LOADING:
            return {
                ...state,
                isLoading: action.payload
            }
        
        case SET_MESSAGE:
            return {
                ...state,
                message: action.payload
            }
        
        default: 
            return state;    
        
    }
}