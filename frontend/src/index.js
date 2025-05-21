import React from 'react';
import ReactDOM from "react-dom/client";
import App from './App';
import {Provider} from "react-redux"
import {BrowserRouter as Router} from "react-router-dom";
import store from "./redux";
import WebSocketWrapper from "./components/WebSocketWrapper";
import reportWebVitals from './reportWebVitals';

import './assets/styles/main.css';
import "./assets/styles/chat.css";
import "./assets/styles/util.css";
import "react-toastify/dist/ReactToastify.css";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
    <Provider store={store}>
        <Router>
            <WebSocketWrapper>
                <App />
            </WebSocketWrapper>
        </Router>
    </Provider>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
