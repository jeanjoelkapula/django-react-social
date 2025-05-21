import React from "react";
import { useSelector } from "react-redux";

export default function ChatHeader(props) {
    const iconStyle = {
        fontSize: "36px",
        color: "#8e8d8d !important"
    }

    return (
        <>
            <div className="flex-grow-0 py-3 pr-4 pl-lg-4" style={{borderBottom: "1px solid #ffffff38"}}>
                <div className="media align-items-center">
                    <a className="chat-sidebox-toggler d-lg-none d-block text-muted text-large px-4 mr-2"><i className="ion ion-md-more" style={iconStyle}></i></a>
                    <div className="position-relative">
                        <span className="badge badge-dot badge-success indicator"></span>
                        <a><i className="fas fa-user-circle"></i></a>
                    </div>
                    <div id="chat-header-username" className="media-body pl-3 text-w">{props.username}</div>
                </div>
            </div>
        </>
    )
}