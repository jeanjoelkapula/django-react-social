import React, { useEffect } from "react";
import {Link} from "react-router-dom";
import { logout } from "../../helpers/fetchHelpers";
import { useDispatch, useSelector } from "react-redux";
import { resetAuth } from "../../redux/userAuth";
import { setModalShown } from "../../redux/postModal";

export default function LeftSideBar(props) {
    const dispatch = useDispatch();
    const chats = useSelector(state => state.chats);
    let unread_count = 0;

    chats.forEach(chat => {
        unread_count += chat.unread_count;
    });

    async function handleLogout () {
        await logout();
        dispatch(resetAuth());
    }

    function openModal() {
        dispatch(setModalShown(true));
    }

    function closeModal() {
        dispatch(setModalShown(false))
    }

    return (
        <div className="twitter-wrap">
            <div className="side-left">
                <ul className="menu">
                    <li className="menu-item">
                        <a className="menu-link">
                            <i className="zmdi zmdi-landscape"></i>
                        </a>
                    </li>

                    <li className="menu-item">
                        <Link to="/" className="menu-link">
                            <i className="fas fa-home"></i>
                        </Link>
                        <Link to="/" className="menu-link-text">
                            <div>
                                <span>All Posts</span>
                            </div>    
                        </Link>
                    </li>

                    <li className="menu-item">
                        <Link to="/following" className="menu-link">
                            <i className="fas fa-people-arrows"></i>
                        </Link>
                        <Link to="/following" className="menu-link-text">
                            <div >
                                <span>Following</span>
                            </div>    
                        </Link>
                    </li>
                    <li className="menu-item">
                        <Link to="/messages" className="menu-link">
                            <i className="far fa-envelope"></i>
                            <span className={`badge chat-badge m-badge menu-icon-badge ${unread_count == 0 && `d-none`}`} id="messages-badge-">{unread_count}</span> 
                        </Link>
                        <Link to="/messages" className="menu-link-text">
                            <div >
                                <span>Messages</span>
                            </div>   
                            <div className={`badge chat-badge m-badge ${unread_count == 0 && `d-none`}`} id="messages-badge-" style={{marginLeft: "5px"}}>{unread_count}</div> 
                        </Link>
                    </li>
                    <li className="menu-item">
                        <Link to="/profile" className="menu-link">
                            <i className="fas fa-user-circle"></i>
                        </Link>
                        <Link to="/profile" className="menu-link-text">
                            <div>
                                <span>Profile</span>
                            </div>    
                        </Link>
                    </li>
                    
                    <li className="menu-item">
                        <a className="menu-link">
                            <i className="fas fa-arrow-circle-left" onClick={handleLogout}></i>
                        </a>
                        <a className="menu-link-text" onClick={handleLogout}>
                            <div >
                                <span>Log out</span>
                            </div>
                        </a>
                    </li>

                    <li className="menu-item">
                        <a className="menu-link add-twit" data-toggle="modal" data-target="#twit-modal" onClick={openModal}>
                            <i className="fas fa-feather-alt"></i>
                        </a>
                    </li>
                    <li className="menu-item ">
                        <button id="menu-twit-button" onClick={openModal} className="add-twit-button" data-toggle="modal" data-target="#twit-modal">
                            New Post
                        </button>
                    </li>
                </ul>
            </div>
        </div>
        
    )
}