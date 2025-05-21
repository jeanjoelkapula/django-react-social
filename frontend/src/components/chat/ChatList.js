import React from "react";
import { useSelector } from "react-redux";
import Chat from "./Chat";

export default function ChatList (props) {
    const chats = useSelector(state => state.chats);
    const currentChat = useSelector(state => state.currentChat);

    const chatElements = chats.map(chat => (
        <Chat key={chat.id} chat={chat} isSelected={chat.id === currentChat.id ? true : false}/>
    ));

    return (
        <>
            {
                chats.length > 0 ?
                chatElements :
                <h4>No Chats</h4>
            }
        </>
    )
}