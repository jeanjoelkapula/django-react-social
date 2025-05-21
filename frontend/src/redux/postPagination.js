const initialState = {
    next: null,
    previous: null,
    results: []
}

const SET_POST_PAGE = "SET_POST_PAGE";

export function setPostPage(payload) {
    return {
        type: SET_POST_PAGE,
        payload
    }
}

export default function postsPaginationReducer(state = initialState, action) {
    switch(action.type) {
        case SET_POST_PAGE:
            return action.payload;
        default:
            return state
    }
}