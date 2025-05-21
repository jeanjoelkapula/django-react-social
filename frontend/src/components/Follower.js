import React from "react";
import { Link } from "react-router-dom";

export default function Follower(props) {
    const {username} = props;

    return (
        <div className="follow-card post">
            <div className="follow-user-icon">
                <Link to={`/profile/${username}/`}><i className="fas fa-user-circle"></i></Link>
            </div>
            <div className="follow-username">
                <div className="post-username">
                    <span><Link to={`/profile/${username}/`}>{username}</Link></span>
                </div>
            </div>          
        </div>
    );
}