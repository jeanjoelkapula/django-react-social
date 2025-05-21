import React from "react";

export default function ChatContainer(props) {

    return (
        <div className="chat-mainbox d-flex col flex-column">
            <div id="chat-mainbox" className="chat-mainbox d-flex col flex-column">
                {props.children}
            </div>
        </div>
    )
}