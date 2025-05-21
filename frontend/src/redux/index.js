import {combineReducers, createStore, applyMiddleware} from "redux";
import thunk from "redux-thunk";
import { reducer as reduxFormReducer } from 'redux-form';
import userAuthReducer from "./userAuth"
import postsReducer from "./posts";
import postsPaginationReducer from "./postPagination";
import chatsReducer from "./chats";
import currentChatReducer from "./currentChat";
import authReducer from "./authForm";
import PostModalReducer from "./postModal";
import profileReducer from "./profile";
import messageCountReducer from "./unreadMessageCount";
import webSocketReducer from "./websocket";

const rootReducer = combineReducers({
    auth: userAuthReducer,
    form: reduxFormReducer,
    authFormData: authReducer,
    posts: postsReducer,
    postPagination: postsPaginationReducer,
    chats: chatsReducer,
    currentChat: currentChatReducer,
    post_modal_shown: PostModalReducer,
    profile: profileReducer,
    webSocket: webSocketReducer,
    unreadMessageCount: messageCountReducer
});

export default createStore(rootReducer, applyMiddleware(thunk));