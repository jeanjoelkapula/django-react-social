import React from "react";

export default function ChatContentWrapper(props) {

    return (
        <div className="layout-content scrollDiv w-100">
            <div className="container-fluid d-flex align-items-stretch flex-grow-1 p-0 h-100">
                <div className="chat-wrapper w-100 h-100">
                    <div className="flex-grow-1 position-relative overflow-hidden w-100 h-100" style={{backgroundCcolor: "black"}}>
                        <div className="row no-gutters h-100">
                            {props.children}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}