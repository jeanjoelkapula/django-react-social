import React from "react";
import {Routes, Route, Navigate} from "react-router-dom";

//components
import AuthBase from "./pages/auth/AuthBase";
import LoginForm from "./components/auth/LoginForm";
import RegisterForm from "./components/auth/RegisterForm";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import Following from "./pages/Following";
import Messages from "./pages/Messages";
import { ToastContainer } from "react-toastify";
import ErrorList from "./components/ErrorList";
import PostForm from "./components/PostForm";
import PostModal from "./components/PostModal";


//hooks
import {useSelector, useDispatch} from "react-redux";
import { useEffect, useContext } from "react";
import { toast } from "react-toastify";

//actions
import {setAuthLoading} from "./redux/authForm";
import { setCurrentUser, setAuthToken } from "./redux/userAuth";
import { addPosts, addPost ,clearPosts, setPosts } from "./redux/posts";
import { setChats } from "./redux/chats";
import { setPostPage } from "./redux/postPagination";
import { connect } from "./redux/websocket";
import { addMessage } from "./redux/chats";
import { setMessageCount } from "./redux/unreadMessageCount";
import { setCurrentChat, addCurrentChatMessage } from "./redux/currentChat";

//helpers
import { login, register } from "./helpers/fetchHelpers";
import { isEmpty } from "./helpers/utils";
import { getPosts, getChats } from "./helpers/fetchHelpers";

//contexts
import WebSocketContext from "./contexts/WebSocketContext";


function App() {

    //to allow hook call not directly in function component
    const dispatch = useDispatch();

    const auth = useSelector(state => state.auth);
    const websocket = useContext(WebSocketContext);
    const chats = useSelector(state => state.chats);
    const currentChat = useSelector(state => state.currentChat);

    useEffect(()=>{
        // check localStorage
        if (!isEmpty(localStorage.getItem("token"))) {
            dispatch(setAuthToken(localStorage.getItem("token")));
            
        }

        if (!isEmpty(localStorage.getItem("user"))) {
            const user = JSON.parse(localStorage.getItem("user"));
            dispatch(setCurrentUser(user));
        }
    },[]);

    useEffect(()=> {
        async function requestChats() {
            var data = await getChats();

            if (data.errors) {
                toast.error(<ErrorList errors={data.errors} />);
            }
            else {
                dispatch(setChats(data.chats));
                dispatch(setMessageCount(data.unread_count));
            }
        }

        if (auth.user) {
            dispatch(connect({auth: auth}));
            requestChats();
        }
    }, [auth.user])

    async function handleLogin(values) {
        
        dispatch(setAuthLoading(true));

        const data = await login (values);

        if (data.errors) {
            toast.error(<ErrorList errors={data.errors} />);
        }
        else {
            dispatch(setAuthToken(data.auth.token));
            dispatch(setCurrentUser(data.auth.user));

        }

        dispatch(setAuthLoading(false));
    }


        if (websocket) {
            websocket.onmessage = event => {
                const message = JSON.parse(event.data);
                dispatch(addMessage(message));
                if (currentChat.id === message.chat) {
                    dispatch(addCurrentChatMessage(message.message));
                }
            }
        }

    async function handleRegister(values) {
        dispatch(setAuthLoading(true));

        const data = await register (values);

        if (data.errors) {
            toast.error(<ErrorList errors={data.errors} />);
        }
        else {
            dispatch(setAuthToken(data.auth.token));
            dispatch(setCurrentUser(data.auth.user));
        }

        dispatch(setAuthLoading(false));
    }

    return (
        <div className="App">
            <ToastContainer hideProgressBar={true} newestOnTop={true} />
            <PostModal />
            <Routes>
                <Route exact path ="/" 
                    element =
                        {
                            auth.user ?
                            <Home following={false} /> :
                            <Navigate to="/login" />
                        }
                />

                <Route path ="/following" 
                    element =
                        {
                            auth.user ?
                            <Home following={true} /> :
                            <Navigate to="/login" />
                        }
                />
                    
                <Route path ="/login" 
                    element =
                        {
                            <AuthBase>
                                {
                                    auth.user ?
                                    <Navigate to="/" />:
                                    <LoginForm onSubmit={handleLogin}/>
                                }
                            </AuthBase>
                        }
                />
                    
                <Route path ="/register"
                    element =
                        {
                            <AuthBase>
                                {
                                    auth.user ?
                                    <Navigate to="/" /> :
                                    <RegisterForm onSubmit={handleRegister}/>
                                }
                            </AuthBase>
                        }
                />

                <Route path ="/profile"
                    element = 
                        {
                            auth.user ?
                            <Profile /> :
                            <Navigate to="/login" />
                        } 
                />

                <Route path ="/profile/:username"
                    element = 
                        {
                            auth.user ?
                            <Profile /> :
                            <Navigate to="/login" />
                        } 
                />

                <Route path ="/profile/:username/:followTab"
                    element = 
                        {
                            auth.user ?
                            <Following /> :
                            <Navigate to="/login" />
                        } 
                />

                <Route path ="/messages"
                    element = 
                        {
                            auth.user ?
                            <Messages /> :
                            <Navigate to="/login" />
                        } 
                />

                <Route path ="/messages/:recipient"
                    element = 
                        {
                            auth.user ?
                            <Messages /> :
                            <Navigate to="/login" />
                        } 
                />
            </Routes>
        </div>
    );
}

export default App;
