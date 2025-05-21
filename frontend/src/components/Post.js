import React from "react";
import { Link } from "react-router-dom";
import { likePost, dislikePost, unlikePost } from "../helpers/fetchHelpers";
import { useSelector, useDispatch } from "react-redux";
import { toast } from "react-toastify";
import ErrorList from "./ErrorList";
import { setPosts } from "../redux/posts";

export default function Post(props) {
    const posts = useSelector(state => state.posts);
    const dispatch = useDispatch();

    const {user, id, date_created, post, is_liked, is_disliked, like_count, dislike_count} = props.post;

    async function handlePostLike() {

        const result = await likePost(id);
        console.log(result);
        if (result.errors) {
            toast.error(<ErrorList errors={result.erros} />);
        }
        else {
            const newPosts = posts.map(item => {
                if (item.id === id) {
                    return {
                        ...item,
                        is_liked: true,
                        is_disliked: false,
                        like_count: result.like_count,
                        dislike_count: result.dislike_count
                    }
                }
                else {
                    return item
                }
            });

            dispatch(setPosts(newPosts));            
        }
    }

    async function handlePostDislike () {
        const result = await dislikePost(id);

        if (result.errors) {
            toast.error(<ErrorList errors={result.erros} />);
        }
        else {
            const newPosts = posts.map(item => {
                if (item.id === id) {
                    return {
                        ...item,
                        is_disliked: true,
                        is_liked: false,
                        like_count: result.like_count,
                        dislike_count: result.dislike_count
                    }
                }
                else {
                    return item
                }
            });

            dispatch(setPosts(newPosts)); 
        }
    }

    async function handlePostUnlike () {
        const result = await unlikePost(id);

        if (result.errors) {
            toast.error(<ErrorList errors={result.erros} />);
        }
        else {
            const newPosts = posts.map(item => {
                if (item.id === id) {
                    return {
                        ...item,
                        is_disliked: false,
                        is_liked: false,
                        like_count: result.like_count,
                        dislike_count: result.dislike_count
                    }
                }
                else {
                    return item
                }
            });

            dispatch(setPosts(newPosts)); 
        }
    }

    return (
        <div className="post">
            <div className="post-user">
                <a href="/profile/4/"><i className="fas fa-user-circle"></i></a>
            </div>
            <div className="post-content">
                <div className="post-username">
                    <Link to={`/profile/${user.username}/`}>{user.username}</Link>
                    <span>{date_created}</span>
                </div>
                <div className="post-text">
                    <p id="post-content-20">{post}</p>
                </div>
                <div className="post-buttons">
                    <div className="post-button">
                        <a id="like-20" data-post="20"><i className={`far fa-heart ${is_liked ? "post-like-active": ""}`}
                            onClick={
                                ()=> {
                                    is_liked ? handlePostUnlike() : handlePostLike ()
                                }
                            }
                        ></i></a>
                        <span>{(like_count > 0) &&  like_count }</span>
                    </div>
                    <div className="post-button">
                        <a id="dislike-20" data-post="20"><i className={`fas fa-heart-broken ${is_disliked ? "post-like-active" : ""}`}
                            onClick={
                                ()=> {
                                    is_disliked ? handlePostUnlike() : handlePostDislike()
                                }
                            }
                        ></i></a>
                        <span>{(dislike_count > 0) && dislike_count}</span>
                    </div>
                </div>
            </div>			
        </div>
    )
}