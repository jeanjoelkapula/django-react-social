const initialState = {
    username: "",
    email: "",
    date_joined: "",
    followees: [],
    followers: []
};

const SET_PROFILE = "SET_PROFILE";

export function setProfile(payload) {
    return {
        type: SET_PROFILE,
        payload
    }
}

export default function profileReducer(state = initialState, action) {
    switch(action.type) {
        case SET_PROFILE:
            return action.payload;
        default:
            return state;
    }
}