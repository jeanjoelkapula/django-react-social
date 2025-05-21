import React from "react";

//Components
import Wrapper from "../components/layout/Wrapper";
import LeftSideBar from "../components/layout/LeftSideBar"
import RightSideBar from "../components/layout/RightSideBar"
import MainContentWrapper from "../components/layout/MainContentWrapper";
import PostsContainer from "../components/PostsContainer";
import ProfileHeader from "../components/ProfileHeader";
import ErrorList from "../components/ErrorList";

//hooks
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useParams, useNavigate } from "react-router-dom";

//actions
import { setPosts } from "../redux/posts";
import { setPostPage } from "../redux/postPagination";
import { setProfile } from "../redux/profile";

//helpers
import { getUserPosts, getProfile } from "../helpers/fetchHelpers";

import { toast } from "react-toastify";


export default function Profile(props) {

    const dispatch = useDispatch();
    const profile = useSelector(state => state.profile);
    const user = useSelector(state => state.auth.user);
    let {username} = useParams();

    useEffect(()=>{
        async function requestProfile() {
            const data = await getProfile(username);
            if (data.errors) {
                toast.error(<ErrorList errors={data.errors} />);
            }
            else {
                dispatch(setProfile(data));
            }
        }    

        if (username !== undefined) {
            requestProfile();
        }
        else {
            dispatch(setProfile(user));
        }

    }, [username]);
    

    useEffect(()=> {
        async function requestPosts() {
            let url = `${profile.username}/posts/`;
            const data = await getUserPosts(url);

            if (data.errors) {
                toast.error(<ErrorList errors={data.errors} />);
            }
            else {
                const {results} = data;
                dispatch(setPostPage(data));        
                dispatch(setPosts(results));
            }
            
        }
        
        if (profile.username !== "") {
            requestPosts();
        }
        
    }, [profile]);
    
    return (
        <Wrapper>
            <LeftSideBar />
            <MainContentWrapper title="Profile">
                <ProfileHeader user = {profile}/>
                <PostsContainer />
            </MainContentWrapper>
            <RightSideBar />
        </Wrapper>
    )
}