import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { followUser } from "../helpers/fetchHelpers";
import ErrorList from "./ErrorList";
import { toast } from "react-toastify";
import { setProfile } from "../redux/profile";
import { setFollowing } from "../redux/userAuth";

export default function ProfileHeader(props) {

    const divStyle = {
        display: "flex",
        marginLeft: "auto"
    };

    const followButtonStyle = {
        marginRight: "0px"
    };

    const dispatch = useDispatch();
    const profile = useSelector(state => state.profile); 
    const user = useSelector(state => state.auth.user);
    const {username, date_joined, followers, followees} = props.user;
    const is_following = profile.followers.includes(user.username);

    async function handleFollowClick() {
        const data = await followUser(username, !is_following);

        if (data.errors) {
            toast.error(<ErrorList errors={data.errros} />);
        }
        else {
            const {follower, followee} = data;
            dispatch(setProfile(followee));
            dispatch(setFollowing({followers:follower.followers, followees: follower.followees}))
        }
    }

    return (
        <div className="profile-top">
            <div className="profile-user">
                <i className="fas fa-user-circle"></i>
            </div>
            <div>
                <div className="profile-username">
                    <span>{username}</span>
                </div>
                <div className="profile-joined-date">
                    <i className="fas fa-calendar-alt"></i><span> Joined {date_joined}</span>
                </div>
                <div className="profile-following">
                    <div>
                        <span id="followees">{followees.length}</span><p><Link to={`/profile/${username}/followees`}>Following</Link></p>
                    </div>
                    <div>
                        <span id="followers">{followers.length}</span><p><Link to={`/profile/${username}/followers`}>Followers</Link></p>
                    </div>
                    {
                        (
                            (profile.username !== user.username) && 
                            <div style={divStyle}>                    
                                <div>
                                    <Link to={`/messages/${profile.username}`} className="profile-message-button">
                                        <i className="far fa-envelope"></i>
                                    </Link>
                                    <a href="/messages?chat='new'&amp;s=1&amp;r=2" >
                                        
                                    </a>
                                </div>
                                {
                                    is_following ?
                                        <div className="unfollow-button">
                                            <button onClick={handleFollowClick}><span style={followButtonStyle}>Following</span></button>
                                        </div>
                                    :
                                    <div className="follow-button">
                                        <button onClick={handleFollowClick}><span style={followButtonStyle}>Follow</span></button>
                                    </div>
                                }
                    
                            </div>
                        )
                    }
                </div>
            </div>
        </div>
    )
}