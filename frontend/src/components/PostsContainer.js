import React, { useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import Post from "./Post";
import NoPostAvailable from "./NoPostAvailable";
import ErrorList from "./ErrorList";
import { useEffect, userRef } from "react";
import { isBottom } from "../helpers/utils";
import { getPosts } from "../helpers/fetchHelpers";
import { toast } from "react-toastify";
import { setPostPage } from "../redux/postPagination";
import { addPosts } from "../redux/posts";

export default function PostsContainer (props) {
    const pagination = useSelector(state => state.postPagination);
    const posts = useSelector(state => state.posts);
    const postElements = posts.map(post => (
        <Post key={post.id} post={post} />
    ));
    
    const containerRef = useRef(null);
    const dispatch = useDispatch();
    async function trackScrolling () {
        if (isBottom(containerRef.current)) {
            if (pagination.next !== null) {
                const data = await getPosts(pagination.next);

                if (data.errors) {
                    toast.error(<ErrorList errors={data.errors} />);
                }
                else {

                    dispatch(setPostPage(data));
                    dispatch(addPosts(data.results));
                }
            }
            
        }
    };

    useEffect(()=>{
        containerRef.current.onscroll = trackScrolling;
    });

    return (
        <div className="post-container disable-scrollbars" ref={containerRef}>
            {
                posts.length > 0 ?
                postElements :
                <NoPostAvailable />
            }
        </div>
    )
}