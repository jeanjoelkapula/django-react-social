import React from "react";

//components
import Wrapper from "../components/layout/Wrapper";
import LeftSideBar from "../components/layout/LeftSideBar";
import MainContentWrapper from "../components/layout/MainContentWrapper";
import RightSideBar from "../components/layout/RightSideBar";
import FollowerContainer from "../components/layout/FollowerContainer";
import { Link } from "react-router-dom";
import ErrorList from "../components/ErrorList";
import { toast } from "react-toastify";

//actions
import { setProfile } from "../redux/profile";

//hooks
import { useSelector, useDispatch } from "react-redux";
import { useParams } from "react-router-dom";
import { useEffect } from "react";

//helpers
import { getProfile } from "../helpers/fetchHelpers";


export default function Following(props) {
    const {username, followTab} = useParams();
    const profile = useSelector(state => state.profile);
    const dispatch = useDispatch();
    const is_followers_tab = (followTab === "followers");
    const is_followees_tab = (followTab === "followees");

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

        requestProfile();

    },[]);

    return (
        <Wrapper>
            <LeftSideBar />
            <MainContentWrapper title={profile.username}>
                <div className="" style={{paddingTop: "15px"}}>
                    <ul className="nav nav-tabs" role="tablist">
                        <li className="nav-item tab-nav">
                            <Link className={`nav-link tab-link ${is_followers_tab && "active"}`} data-toggle="tab" to={`/profile/${profile.username}/followers`} role="tab">Followers</Link>
                        </li>
                        <li className="nav-item tab-nav">
                            <Link className={`nav-link tab-link ${is_followees_tab && "active"}`} data-toggle="tab" to={`/profile/${profile.username}/followees`} role="tab">Following</Link>
                        </li>

                    </ul>
                    <div className="tab-content">
                        <FollowerContainer items={profile.followers} is_active={is_followers_tab}/>
                        <FollowerContainer items={profile.followees} is_active={is_followees_tab}/>
                    </div>
                </div>
            </MainContentWrapper>
            <RightSideBar />
        </Wrapper>
    )
}