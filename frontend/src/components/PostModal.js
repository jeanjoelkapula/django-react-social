import React from "react";
import PostForm from "./PostForm";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "react-toastify";
import ErrorList from "./ErrorList";
import { addPost } from "../redux/posts";
import { createPost } from "../helpers/fetchHelpers";
import { setModalShown } from "../redux/postModal";

export default function PostModal () {
    const post_modal_shown = useSelector(state => state.post_modal_shown);
    const dispatch = useDispatch();

    const style = {
        display: post_modal_shown ? "block" : "none"
    };

    function closeModal() {
        dispatch(setModalShown(false));

    }

    async function handleCreatePost(values) {
        const data = await createPost(values);

        if (data.errors) {
            toast.error(<ErrorList errors={data.errors} />);
        }
        else {
            dispatch(addPost(data.post));
            closeModal();
        }
    }

    return (
        <div id="twit-modal" className="modal post-modal" tabIndex="-1" role="dialog" style={style}>
            <div className="modal-dialog" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <button onClick={closeModal} type="button" className="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">×</span>
                        </button>
                    </div>
                    <div className="modal-body">
                        <PostForm onSubmit={handleCreatePost}/>
                    </div>
                </div>
            </div>
        </div>
    );
}