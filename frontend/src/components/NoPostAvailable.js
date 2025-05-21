import React from "react";

export default function NoPostAvailable() {

    const divStyle = {
        display: "flex",
        height: "100%",
        justifyContent: "center",
        alignItems: "center"
    }

    const spanStyle = {
        color: "white",
        fontSize: "30px"
    }

    return (    
        <div style={divStyle}>
            <span style={spanStyle}>No Posts available</span>
        </div>
    )
}