import React from "react";

export default function NoChatSelected() {

    return (
        <div id="unselected-chat-container" className="unselected-chat-container">
            <div>
                <span className="header text-white" style={{fontSize:"40px"}}>You don’t have a<br/> chat selected</span>
            </div>
            <div>
                <span className="chat-text p">Choose one from your existing chats</span>
            </div>
        </div>
    )
}