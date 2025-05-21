import React from "react";
import { useRef, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import Message from "./Message";
import ErrorList from "../ErrorList";
import { setMessagesRead } from "../../helpers/fetchHelpers";
import { updateMessagesReadStatus } from "../../redux/chats";
import {toast} from "react-toastify";
export default function MessageList(props) {

    const user = useSelector(state => state.auth.user);
    const currentChat = useSelector(state => state.currentChat);
    const messageEndRef = useRef(null);
    const dispatch = useDispatch();
    const messageElements = props.messages.map(message => (
        <Message 
            key = {message.id}
            message = {message}
        />
    ));

    let unread_count = 0;
    props.messages.forEach(message => {
        if (message.read == false && user.username == message.recipient) {
            unread_count += 1;
        }
    });


    useEffect(() => {

        async function updateMessagesStatus() {
            const data = await setMessagesRead(currentChat.id, true);

            if (data.errors) {
                toast.error(<ErrorList errors={data.errors} />);
            }
            else {
                dispatch(updateMessagesReadStatus({
                    chat: currentChat.id,
                    
                }))
            }
        }
        messageEndRef.current?.scrollIntoView({ behavior: 'smooth' , block: 'end'});

        if (unread_count > 0) {
            updateMessagesStatus();
        }
    });

    return (
        <div className="flex-grow-1 position-relative">
            <div id="message-list" className="chat-messages chat-scroll custom-scrollbar p-4 ps">
                {messageElements}
                <div ref={messageEndRef}/>
            </div>
        </div>
    )
}