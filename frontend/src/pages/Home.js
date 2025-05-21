import React, {useEffect} from "react";
import Wrapper from "../components/layout/Wrapper";
import LeftSideBar from "../components/layout/LeftSideBar"
import RightSideBar from "../components/layout/RightSideBar"
import MainContentWrapper from "../components/layout/MainContentWrapper";
import PostForm from "../components/PostForm";
import PostsContainer from "../components/PostsContainer";
import ErrorList from "../components/ErrorList";

//actions
import { addPost, setPosts } from "../redux/posts";
import { setPostPage } from "../redux/postPagination";

//helpers
import { createPost, getPosts, getFollowingPosts } from "../helpers/fetchHelpers";
import { toast } from "react-toastify";

//hooks
import { useDispatch, useSelector } from "react-redux";

export default function Home(props) {
    const dispatch = useDispatch();
    const auth = useSelector(state => state.auth);
    const {following} = props;

    async function handleCreatePost(values) {
        const data = await createPost(values);

        if (data.errors) {
            toast.error(<ErrorList errors={data.errors} />);
        }
        else {
            dispatch(addPost(data.post));
        }
    }

    useEffect(()=> {
        async function requestPosts() {
            let page;
            if (following) {
                page = await getFollowingPosts();
            }
            else {
                page = await getPosts();
            }
             
            const {results} = page;
            dispatch(setPostPage(page));        
            dispatch(setPosts(results));
            
        }
        
        if (auth.user) {
            requestPosts();
        }
        
    });

    return (
        <Wrapper>
            <LeftSideBar />
            <MainContentWrapper title="Home">
                <PostForm onSubmit={handleCreatePost}/>
                <PostsContainer />
            </MainContentWrapper>
            <RightSideBar />
        </Wrapper>
    )
}