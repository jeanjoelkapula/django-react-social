# Django REST Twitter Backend

This is a fully-featured Django REST API backend for a Twitter-like social media platform. The project supports real-time chat, social relationships (follows), posting, likes/dislikes, and robust user management. It is designed as a modern, extensible backend for a single-page React frontend, and is a significant extension of Harvard's CS50W "Network" project.

## Features

- **User Authentication**  
  Register, login, and logout with secure password management and token-based authentication.

- **User Profiles & Social Graph**  
  - Follow/unfollow users (non-symmetrical)
  - View detailed profiles, including follower/followee lists

- **Post Management**  
  - Create, edit, and fetch posts
  - Like, dislike, or remove like/dislike from posts
  - Feeds: global, personal (following), and by user

- **Real-Time Chat**  
  - Direct and group messaging between users
  - Unread message tracking and notification
  - WebSocket-based chat using Django Channels

- **API-first Design**  
  - All features are exposed through RESTful endpoints, designed for modern SPA frontends

- **Business Logic Separation**  
  - Clean separation of validation, business logic, and API representation using serializers and services

---

## Project Structure
  ```bash
  django-rest-twitter/
  ├── api/ # Main Django app: models, API logic, serializers, chat consumers
  │ ├── migrations/ # Database migration history
  │ ├── templates/ # index.html (SPA entry point for frontend)
  │ ├── admin.py # Django admin integration
  │ ├── apps.py # Django app configuration
  │ ├── consumers.py # Django Channels WebSocket consumers (real-time chat)
  │ ├── models.py # Database models: User, Post, PostLike, Chat, ChatMessage
  │ ├── routing.py # ASGI WebSocket routing
  │ ├── serializers.py # DRF serializers for input validation and API output
  │ ├── services.py # Core business logic for users, posts, and chat
  │ ├── tests.py # (To be implemented) Unit and integration tests
  │ ├── urls.py # App-level API routing
  │ ├── views.py # API endpoint implementations
  ├── rest_twitter/ # Project settings and ASGI/WSGI config
  │ ├── asgi.py
  │ ├── channels_auth_middleware.py
  │ ├── settings.py
  │ ├── urls.py
  │ ├── util.py
  │ ├── wsgi.py
  ├── manage.py # Django project manager
  ├── requirements.txt # Python package requirements
  ├── README.md 
  ```
---

## API Overview

**Authentication:**  
- `POST /auth/register/` — Register new user  
- `POST /auth/login/` — Login, receive API token  
- `GET  /auth/logout/` — Logout, invalidate token  

**User & Social:**  
- `GET  /<username>/profile/` — Get profile, followers, followees  
- `PUT  /<username>/follow/` — Follow or unfollow a user  

**Posts:**  
- `GET  /posts/` — List all posts  
- `GET  /posts/following/` — Feed: posts by users you follow  
- `GET  /<username>/posts/` — Posts by user  
- `POST /post/` — Create a post  
- `PUT  /post/<id>/` — Edit a post  
- `PUT  /post/<id>/like/` — Like or dislike a post  
- `PUT  /post/<id>/unlike/` — Remove like/dislike  

**Chat & Messaging:**  
- `GET  /chats/` — List your chat threads  
- `PUT  /messages/<chat_id>/status/` — Mark all messages in chat as read  
- `WebSocket: /ws/chat/<username>/` — Real-time chat (Django Channels)

---

## Key Technologies

- **Django 3+ / Django REST Framework** — Modern Python web API framework  
- **Django Channels** — WebSockets for real-time communication  
- **Token Authentication** — Stateless, scalable API sessions  
- **PostgreSQL** (recommended) — Production-grade relational DB (works with SQLite for dev)

---

## Setup & Development

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/django-rest-twitter.git
   cd django-rest-twitter

2. Install Dependencies
    It’s recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. Run Migrations
    ```bash
    python manage.py migrate

4. Create a Superuser (optional)
    ```bash
    python manage.py createsuperuser

5. Run the Development Server
    ```bash
    python manage.py runserver

About This Project

This backend was designed and built as a capstone and learning project by Jean Joel Kapula. It demonstrates the use of modern Django for scalable, API-first social platforms, with clear code structure and focus on extensibility and real-world web application patterns.