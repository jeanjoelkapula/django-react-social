import React from "react";
import {reduxForm, Field} from "redux-form";

import { useContext } from "react";


let MessageForm = props => {

    const inputStyle = {
        height: "55px",
        backgroundColor: "black", 
        color: "white"
    }
    const {handleSubmit} = props;
    
    return (
        <div className="flex-grow-0 py-3 px-4" style={{borderTop: "1px solid #ffffff38"}}>
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <Field id="chat-message-input" component="input" name="message" type="text" className="form-control chat-input" placeholder="Type your message" style={inputStyle} />
                    <div className="input-group-append">
                        <button type="submit">
                            <a id="chat-message-submit" className="chat-send">
                                <i className="fas fa-feather-alt"></i>
                            </a>
                        </button>       
                    </div>
                </div>
            </form>
        </div>
    )
}

MessageForm = reduxForm({
    form: "messageForm"
}) (MessageForm)

export default MessageForm