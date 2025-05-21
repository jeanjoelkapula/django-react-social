import React from "react"
import { reduxForm, Field } from 'redux-form';

let PostForm = props => {

    const {handleSubmit} = props;

    return (
        <div className="twit-form-container">
            <form action="/" method="POST" onSubmit={handleSubmit}>
                <div className="write-twit">
                    <div className="post-user icon-div">
                        <i className="fas fa-user-circle"></i>
                    </div>
                    <Field name="post" id="post" cols="30" rows="3" type="text" component="textarea" placeholder="what's happening?" />	
                </div>
                <div className="modal-button-container">
                    <button className="add-twit-button modal-button" type="">
                        New Post
                    </button>
                </div>
            </form>
        </div>

    )
}

PostForm = reduxForm({
    form: 'postForm'
})(PostForm)

export default PostForm