import React from "react";

export default function MainContentWrapper(props) {
    return (
        <div className="side-main"> 
            <div className="top-fixed">
                <h4 className="link-home">{props.title}</h4>
            </div>
            <div className="">
                {props.children}
            </div>
        </div>
    )
}