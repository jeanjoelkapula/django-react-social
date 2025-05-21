import {POST, GET } from './axios.js';

const headers = {

}
export async function login(data) {
    const url = "auth/login/";
    const result = await POST(url, data);

    return result;
}

export async function logout() {
    const url = "auth/logout/";
    const result = await GET(url);

    return result;
}

export async function register (data) {
    const url = "auth/register/";
    const result = await POST(url, data);

    return result;
}

export async function getPosts(url = "posts/") {
    var relative_path = true;

    if (url !=="posts/") {
        relative_path = false;
    }
    const result = await GET(url, relative_path);

    return result;
}

export async function getFollowingPosts(url = "posts/following") {
    var relative_path = true;

    if (url !=="posts/following") {
        relative_path = false;
    }
    const result = await GET(url, relative_path);

    return result;
}

export async function getUserPosts(url) {
    var relative_path = true;

    if (url.includes("http")) {
        relative_path = false;
    }
    const result = await GET(url, relative_path);

    return result;
}

export async function createPost(data) {
    const url = "post/";
    const result = await POST(url, data);

    return result;
}

export async function likePost(post) {
    const url = `post/${post}/like/`;
    const data = {
        is_like: true
    };
    const result = await POST(url,data, "PUT");

    return result;
}

export async function dislikePost(post) {
    const url = `post/${post}/like/`;
    const data = {
        is_like: false
    };
    const result = await POST(url,data, "PUT");

    return result;
}

export async function unlikePost(post) {
    const url = `post/${post}/unlike/`;

    const data = {
        unlike: true
    };
    const result = await POST(url,data, "PUT");

    return result;
}

export async function getProfile(username) {
    const url = `${username}/profile/`;

    const result = await GET(url);

    return result;
}

export async function followUser(username, follow=true) {
    const url = `${username}/follow/`;
    const data = {
        follow
    };

    const result = await POST(url, data, "PUT");

    return result;
}

export async function getChats() {
    const url = "chats/";

    const result = await GET(url);

    return result;
}

export async function setMessagesRead(chat, read) {
    const url = `messages/${chat}/status/`;

    const data = {
        read
    };

    const result = await POST(url, data, "PUT");

    return result;
}