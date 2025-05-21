import React from "react";
import { useSelector } from "react-redux";

import { Link } from "react-router-dom";

export default function Chat(props) {
    const username = useSelector(state => state.auth.user.username); 
    const {chat} = props;
    const participant = chat.participants.find(x => x !== username);
    
    return (
        <Link className={`list-group-item list-group-item-action ${props.isSelected && "active"}`} to={`/messages/${participant}`}>
            <i className="fas fa-user-circle"></i>
            <div className="media-body ml-3">
                <span key={participant}>{participant}</span>
            </div>
            <div className={`badge chat-badge ${chat.unread_count == 0 && `d-none`}`}>{chat.unread_count}</div>
        </Link>
    )
}