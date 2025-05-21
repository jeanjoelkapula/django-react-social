import { setAxiosAuthToken } from "../helpers/axios";

const initialState = {
    user: null,
    token: "",
}

const SET_TOKEN = "SET_TOKEN";
const SET_USER = "SET_USER";
const RESET = "RESET";
const SET_FOLLOWING = "SET_FOLLOWING";

export function setAuthToken(payload) {
    return (dispatch) => {
        setAxiosAuthToken(payload);
        localStorage.setItem("token", payload);

        dispatch({
            type: SET_TOKEN,
            payload: payload
        });
    }
}

export function setCurrentUser(payload) {
    return (dispatch) => {
        localStorage.setItem("user", JSON.stringify(payload));

        dispatch({
            type: SET_USER,
            payload: payload
        });
    }
}

export function resetAuth() {
    return (dispatch) => {
        setAxiosAuthToken("");
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        
        dispatch({
            type: RESET
        });
    }
}

export function setFollowing(payload) {
    return {
        type: SET_FOLLOWING,
        payload
    }
}


export default function userAuthReducer (state = initialState, action) {
    switch(action.type) {
        case SET_TOKEN:
            return {
                ...state,
                token: action.payload
            }
        case SET_USER: 
            return {
                ...state,
                user: action.payload
            }
        case RESET:
            return initialState
        case SET_FOLLOWING:
            return {
                ...state,
                user: {
                    ...state.user,
                    followers: action.payload.followers,
                    followees: action.payload.followees
                }
            }
        default:
            return state
    }
}