const initialState = [];
const ADD_POST = "ADD_POST";
const ADD_POSTS = "ADD_POSTS";
const CLEAR_POSTS = "CLEAR_POSTS";
const SET_POSTS = "SET_POSTS";

export function addPost(payload) {
    return {
        type: ADD_POST,
        payload
    }
}
export function addPosts(payload) {
    return {
        type: ADD_POSTS,
        payload
    }
}

export function clearPosts() {
    return {
        type: CLEAR_POSTS,
    }
}

export function setPosts (payload) {
    return {
        type: SET_POSTS,
        payload
    }
}

export default function postsReducer(state = initialState, action) {
    switch(action.type) {
        case ADD_POST:
            return [
                action.payload,
                ...state
            ]
        case ADD_POSTS:
            return [
                ...state,
                ...action.payload
            ];
        case CLEAR_POSTS:
            return [];
        case SET_POSTS:
            return action.payload;
        default:
            return state;
    }
}