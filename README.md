# Django + React Twitter Social App

This project is a full-stack, Twitter-inspired social network built with a Django REST Framework backend and a React SPA frontend.  
It began as an extension of Harvard CS50 Web's "Network" project and has been re-engineered for modern best practices, modularity, and extensibility.

---

## Tech Stack

- **Backend:** Django 3+, Django REST Framework, Channels, Python 3.x
- **Frontend:** React 17+, React Router, Axios (or fetch), JavaScript (ES6+)
- **DevOps/Tooling:** Node.js, npm, virtualenv

---

## Features

- **User Authentication:** Register, login, and logout with secure token authentication.
- **Social Graph:** Follow/unfollow users; view followers and following lists.
- **Post Management:** Create, edit, and view posts; like/dislike; view personalized feeds.
- **Real-Time Chat:** Direct and group messaging via WebSockets (Django Channels).
- **Profile Pages:** User profiles displaying posts, social links, and stats.
- **API-First Design:** Clean REST API consumed by a modern React SPA frontend.
- **Extensible & Modular:** Well-structured codebase for easy feature additions.

---

## Architecture

> **Full-Stack Architecture**
>
> - **Backend** exposes a stateless, RESTful API with token authentication, plus real-time endpoints using Django Channels for chat.
> - **Frontend** is a single-page React app, making async API calls for all features, and connects to chat endpoints via WebSocket.
> - **Business logic** is separated from API logic for maintainability and clarity.

```
repo-root/
├── backend/ # Django REST API + Channels for real-time features
│ ├── api/ # Main app: models, API views, chat, business logic
│ ├── rest_twitter/ # Project settings, routing, server entrypoints
│ ├── manage.py
│ └── requirements.txt
├── frontend/ # React SPA
│ ├── public/
│ ├── src/
│ │ ├── components/ # Feed, Post, Profile, Chat, etc.
│ │ ├── api/ # API wrappers
│ │ ├── utils/ # Auth and helper functions
│ │ └── App.js
│ └── package.json
└── README.md
```


---

## How This Builds on CS50W "Network"

This project started from Harvard's [CS50 Web Programming with Python and JavaScript "Network"](https://cs50.harvard.edu/web/2020/projects/4/network/) assignment, but expands far beyond:

- **Decoupled Backend & Frontend:**  
  Migrated from a monolithic Django+JS app to a fully separated REST API and React SPA for best-practice scalability and maintainability.
- **Expanded Features:**  
  - Real-time chat using Django Channels (WebSockets).
  - REST API supporting rich user, post, and feed interactions.
  - Modular, reusable React components and a true SPA architecture.
  - Clean separation of concerns with a business logic layer in Django.
- **Professional Readiness:**  
  Project is structured with industry best-practices for version control, extensibility, and maintainability.

---

## Setup Instructions

### Backend (Django)

1. **Install dependencies:**
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2. **Run migrations:**
    ```bash
    python manage.py migrate
    ```
3. **Create a superuser (optional, for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
4. **Start the development server:**
    ```bash
    python manage.py runserver
    ```
5. **(For real-time chat)**  
    Use Django Channels with an ASGI server (e.g., Daphne or Uvicorn).

---

### Frontend (React)

1. **Install dependencies:**
    ```bash
    cd frontend
    npm install
    ```
2. **Start the development server:**
    ```bash
    npm start
    ```
    - By default, this runs on [localhost:3000](http://localhost:3000).

3. **Configure Backend API URL:**
    - Update the API base URL in `/frontend/src/api/api.js` or via a `.env` file for different environments.

---

## Deployment Suggestions

While this project has not yet been deployed in production, it is designed for straightforward deployment.  
**Recommended next steps for deployment:**

- **Dockerization:**  
  Add `Dockerfile` for backend and frontend to enable containerized deployments.
- **CI/CD:**  
  Use GitHub Actions, GitLab CI, or similar for continuous integration and deployment.
- **Backend Production:**  
  Deploy using Gunicorn + Daphne/Uvicorn (for Django Channels/WebSocket support).
- **Frontend Production:**  
  Serve the React build via NGINX or static hosts like Netlify/Vercel.
- **Environment Configuration:**  
  Use environment variables for secrets, API endpoints, and settings.

---

## Improvements & Next Steps

- Add automated testing (backend: pytest/DRF; frontend: Jest/React Testing Library).
- Improve API documentation (Swagger/OpenAPI, DRF docs).
- Upgrade authentication to JWT for more scalable security.
- Make UI more responsive and accessible for all devices.
- Expand real-time features (e.g., typing indicators, message notifications).
- Add deployment scripts and cloud configuration (Heroku, AWS, DigitalOcean, etc).

---

## Folder & File Reference

### Backend Highlights

- **api/models.py:**  
  Defines all main data structures:
  - `User`: Extends Django’s user model with follower/following relationships.
  - `Post`: User-authored content (supports like/dislike).
  - `PostLike`: Tracks individual user likes/dislikes.
  - `Chat` & `ChatMessage`: Group and direct messaging models with read/unread tracking.

- **api/services.py:**  
  Core business logic for all social and messaging features:
  - Handles follow/unfollow, post creation/editing, feed generation, like/dislike logic.
  - Abstracts business rules away from API views/serializers for clarity and reusability.

- **api/consumers.py & routing.py:**  
  Implements Django Channels for real-time WebSocket chat:
  - Handles live chat connections, message broadcasting, and delivery.

- **api/serializers.py:**  
  Serializes and validates data between frontend and backend:
  - Supports custom user, post, like, and chat representations for the API.

- **api/views.py & urls.py:**  
  REST API endpoints for all core app features:
  - User registration, login, profile, follow/unfollow.
  - Post CRUD, likes/dislikes, personal and global feeds.
  - Chat thread access and unread message tracking.

- **rest_twitter/settings.py:**  
  Django project settings, including REST Framework, Channels, authentication, and CORS.

- **rest_twitter/asgi.py & wsgi.py:**  
  Entrypoints for async (Channels/WebSocket) and sync (traditional WSGI) hosting.

---

### Frontend Highlights

- **src/components/**  
  All major UI modules:
  - `Feed.js`: Displays main or personalized feed.
  - `Post.js`: Individual post (view, like/dislike, interact).
  - `Profile.js`: User profile with follower/following details.
  - `Chat.js`: Live messaging (WebSocket integration).
  - `Login.js`, `Register.js`: Auth forms.
  - Additional shared components (navigation, notifications, etc).

- **src/api/**  
  Single location for all backend interaction:
  - Exports functions for auth, posting, following, chat, etc.
  - Centralizes base URL config for easy API switching.

- **src/utils/**  
  Helper utilities:
  - Manages localStorage/session tokens.
  - Provides reusable logic for formatting, websocket connection, etc.

- **App.js:**  
  Top-level React component:
  - Configures routing (using React Router).
  - Handles auth context, navigation, and page layout.

---

## License

[MIT License](LICENSE)

---

## Credits

Originally based on Harvard’s CS50W "Network" project.  
Expanded and refactored for modern web development best practices by Jean Joel Kapula.

---

*For questions or contributions, please open an issue or pull request!*
