import React from "react";

import Follower from "../Follower";

export default function FollowerContainer(props) {
    const followerElements = props.items.map((username, index) => {
        return (<Follower key={index} username={username} />)
    });

    return (
        <div className={`tab-pane ${props.is_active && "active"} disable-scrollbars`} id="followers" role="tabpanel" style={{maxHeight: "800px"}}>
            {followerElements}
        </div>
    );
}