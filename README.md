# Django + React Twitter Social App

This project is a full-stack, Twitter-inspired social network built with a Django REST Framework backend and a React SPA frontend.  
It began as an extension of Harvard CS50 Web's "Network" project and has been re-engineered for modern best practices, modularity, and extensibility.

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

```bash
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
  User, Post, PostLike, Chat, and ChatMessage models with clear relationships and methods.
- **api/services.py:**  
  Central business logic (follows, post CRUD, like/dislike, feed assembly, chat/message handling).
- **api/consumers.py & routing.py:**  
  Django Channels consumers for real-time chat over WebSockets.
- **api/serializers.py:**  
  Django REST Framework serializers for all data models, enabling validation and JSON conversion.
- **api/views.py & urls.py:**  
  DRF API views and endpoint routing for all core functionality.
- **rest_twitter/settings.py:**  
  Project configuration, installed apps, middleware, CORS, and Channels setup.

### Frontend Highlights

- **src/components/**  
  Modular React components (Feed, Post, Profile, Chat, Login, Register, etc).
- **src/api/**  
  Centralized API request functions (login, follow, post, chat, etc).
- **src/utils/**  
  Helper functions (e.g., for authentication token management, websocket setup).
- **App.js:**  
  SPA routing and global logic.

---

## License

[MIT License](LICENSE)

---

## Credits

Originally based on Harvard’s CS50W "Network" project.  
Expanded and refactored for modern web development best practices by Jean Joel Kapula.

---

*For questions or contributions, please open an issue or pull request!*
