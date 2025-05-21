import React from "react";

export default function Message(props) {

    const message = {...props.message}
    const orientation = message.incoming ? "chat-message-left" : "chat-message-right";

    return (
        <div className={`${orientation} mb-4`}>
            <div>
                <a><i className="fas fa-user-circle"></i></a>
                <div className="text-muted  text-nowrap mt-2">{message.time}</div>
            </div>
            <div className="chat-text flex-shrink-1 chat-item rounded py-2 px-3 mr-3">
                <div className="font-weight-semibold mb-1 chat-text-username">{message.user}</div>
                {message.message}
            </div>
        </div>
    )
}