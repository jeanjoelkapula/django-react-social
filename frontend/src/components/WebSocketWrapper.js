import React, {createContext, useState} from "react";
import { useSelector } from "react-redux";
import {WebSocketProvider} from "../contexts/WebSocketContext";

export default function WebSocketWrapper(props) {

    const webSocket = useSelector(state => state.webSocket);

    return (
        <WebSocketProvider value={webSocket}>
            {props.children}
        </WebSocketProvider>
    )
}
