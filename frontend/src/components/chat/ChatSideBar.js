import React from "react";
import ChatList from "./ChatList";

export default function ChatSideBar(props) {


    return (
        <div className="chat-sidebox col">
            <div className="flex-grow-0 px-4">
                <div className="media align-items-center">
                    <div className="media-body" style={{height: "76px"}}>
                    </div>
                    <a className="chat-sidebox-toggler d-lg-none d-block text-muted text-large font-weight-light pl-3">×</a>
                </div>
            </div>
            <div className="flex-grow-1 position-relative">
                <div id="chat-list" className="chat-contacts list-group disable-scrollbars py-3 ps">
                    <ChatList />      
                </div>  
            </div>
        </div>
    )
}