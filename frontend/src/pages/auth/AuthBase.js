import React from "react";
import image from "../../assets/images/bg-01.jpg"

export default function AuthBase(props) {
    
    const divStyle = {
        color: 'blue',
        backgroundImage: 'url(' + image + ')',
    };

    return (
        <div className="container-auth" style={divStyle}>
            <div className="wrap-auth">
                {props.children}
            </div>
        </div>
    )
}