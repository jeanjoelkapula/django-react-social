import React from "react";

//hooks
import { useEffect, useContext } from "react";
import { useSelector, useDispatch } from "react-redux/es/exports";
import { useParams } from "react-router-dom";

//components
import Wrapper from "../components/layout/Wrapper";
import LeftSideBar from "../components/layout/LeftSideBar";
import ChatContentWrapper from "../components/layout/ChatContentWrapper";
import ChatSideBar from "../components/chat/ChatSideBar";
import ChatContainer from "../components/chat/ChatContainer";
import NoChatSelected from "../components/chat/NoChatSelected";
import MessageForm from "../components/chat/MessageForm";
import ChatHeader from "../components/chat/ChatHeader";
import MessageList from "../components/chat/MessageList";
import ErrorList from "../components/ErrorList";

//helpers
import { getChats } from "../helpers/fetchHelpers";

//actions
import { setCurrentChat } from "../redux/currentChat";
import { addChat } from "../redux/chats";
import { reset } from "redux-form";

import { toast } from "react-toastify";

//contexts
import WebSocketContext from "../contexts/WebSocketContext";

export default function Messages(props) {
    const websocket = useContext(WebSocketContext);
    const chats = useSelector(state => state.chats);
    const {recipient} = useParams();
    const dispatch = useDispatch();
    const currentUser = useSelector(state => state.auth.user);
    let currentChat = useSelector(state => state.currentChat);

    Array.prototype.move = function(from, to) {
        this.splice(to, 0, this.splice(from, 1)[0]);
    };

    useEffect(()=>{
        if ((recipient !== undefined)) {
            let chat = chats.find(chat => chat.participants.includes(currentUser.username) && chat.participants.includes(recipient))
            
            if (chat){
                const from = chats.findIndex(c =>  chat.id == c.id);
                
                dispatch(setCurrentChat(chat));
                chats.move(from, 0);
            }
            else {
                chat = {
                    id: 0,
                    participants: [recipient, currentUser.username],
                    chat_messages: []
                };
        
                dispatch(addChat(chat));
                dispatch(setCurrentChat(chat));
            }
    
        }
    },[recipient]); 

    
    async function handleSendMessage(values) {
        const data = {
            chat: currentChat.id,
            recipient: recipient,
            message: values.message
        };

        websocket.send(JSON.stringify(data));
        dispatch(reset('messageForm'));
    }

    

    return (
        <Wrapper>
            <LeftSideBar />
            <ChatContentWrapper>
                <ChatSideBar />
                {
                    (recipient === undefined) ?
                        <ChatContainer>
                            <NoChatSelected/>
                        </ChatContainer>
                        :
                    <ChatContainer>
                        <ChatHeader username={recipient}/>
                        <MessageList messages={ recipient === undefined ? [] : currentChat.chat_messages}/>
                        <MessageForm onSubmit={handleSendMessage}/>
                    </ChatContainer>
                }
                
            </ChatContentWrapper>
        </Wrapper>
    )
}