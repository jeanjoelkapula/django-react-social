# CLAUDE.md

Guidance for AI coding tools and new contributors working in this repo.

## What this is

A Twitter-style social app: Django REST Framework + Django Channels backend, React (Create React App, Redux) frontend. It extends the Harvard CS50W "Network" project. Features: register/login (token auth), posts, like/dislike, follow/unfollow, following feed, paginated feeds, and real-time direct chat over WebSockets.

## Layout

```
backend/
  manage.py
  requirements.txt
  rest_twitter/   settings, urls, asgi (HTTP + WebSocket routing), channels_auth_middleware.py
  api/            models.py, services.py, serializers.py, views.py, urls.py,
                  consumers.py + routing.py (WebSocket chat), tests.py
frontend/
  src/pages/      Home, Following, Profile, Messages, auth/
  src/components/ Post, PostsContainer, PostForm, chat/, layout/ ...
  src/redux/      one file per slice (posts, chats, userAuth, websocket ...)
  src/helpers/    fetchHelpers.js (API calls), axios.js
  src/URL_config.js  API and WebSocket base URLs
```

Backend structure: views are thin and delegate to `api/services.py` (`UserService`, `PostService`, `ChatService`). Put business logic in services, not views or serializers.

## Requirements

- Python 3.13 (pins in `requirements.txt` are verified on 3.13.3) and Node 22.
- Redis for chat, **or** set `CHANNEL_LAYER=memory` to use the in-memory channel layer (single process only: fine for tests, CI and local dev, not for production). On Windows, Memurai is a Redis-compatible server.

## Run it

Backend (from `backend/`):

```bash
python -m venv venv
source venv/bin/activate          # Windows (Git Bash): source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
CHANNEL_LAYER=memory python manage.py runserver 8000   # drop the variable if Redis is running
```

Frontend (from `frontend/`):

```bash
npm ci --legacy-peer-deps         # the flag is required: redux-form@8 declares a React 16/17 peer dependency
npm start                         # http://localhost:3000
```

The frontend has the API address hardcoded to `http://127.0.0.1:8000/api` and WebSocket address to `ws://127.0.0.1:8000/ws/chat/` (`frontend/src/URL_config.js`, `frontend/src/helpers/axios.js`). Run the backend on port 8000.

On Windows, create the venv at a short path if `python -m venv` fails with an `ensurepip` error: long paths (for example inside a deep OneDrive folder) can break it.

## Test it

Backend (from `backend/`):

```bash
CHANNEL_LAYER=memory python manage.py test
python manage.py check
python manage.py makemigrations --check --dry-run   # fails if a model change has no migration
```

Frontend (from `frontend/`):

```bash
CI=true npm test -- --watchAll=false
npm run build
```

Known gotchas:
- Jest silently finds zero tests if the project path contains a folder starting with a dot (for example a `.claude/worktrees/...` checkout). Run from a normal path.
- `npm run build` succeeds with lint warnings, but `CI=true npm run build` exits 1 because Create React App treats warnings as errors when `CI` is set (GitHub Actions sets it automatically). Fix the warnings or unset `CI` for the build step before relying on it in CI.
- The frontend test suite is currently a leftover starter test and does not pass (jest cannot load the ES module `react-redux/es/exports` imported by `src/pages/Messages.js`). Do not treat a frontend test failure as caused by your change until you have checked it against `main`.

## API cheat sheet

Auth: `Authorization: Token <token>`; the token comes from `POST /api/auth/login/` or `/api/auth/register/`.

| Action | Request |
|---|---|
| Register / login | `POST /api/auth/register/`, `POST /api/auth/login/` with `username`, `password` (register also `email`) |
| Feeds (paginated, page size 7) | `GET /api/posts/`, `/api/posts/following/`, `/api/<username>/posts/` |
| Create post | `POST /api/post/` with `{"post": "text"}` |
| Like / dislike | `PUT /api/post/<id>/like/` with `{"is_like": true|false}` |
| Unlike | `PUT /api/post/<id>/unlike/` with `{"unlike": true}` |
| Follow / unfollow | `PUT /api/<username>/follow/` with `{"follow": true|false}` |
| Chats | `GET /api/chats/` |
| WebSocket chat | `ws://127.0.0.1:8000/ws/chat/<your-username>/?token=<token>`; send `{"chat", "recipient", "message"}` |

Current behavior to be aware of: many validation failures and not-found cases return HTTP 200 with an `errors` body, and the frontend reads them that way. Do not change status codes as a drive-by in an unrelated PR.

## Conventions

- Keep changes small and focused: one concern per PR.
- Bug fixes: write the failing test first, see it fail for the right reason, then fix.
- PR description has three parts: **What changed**, **Why**, **How it was verified** (the commands you ran and their result).
- Match the surrounding code's style; do not reformat files you are not otherwise changing.
- Never commit secrets, real credentials or personal data. `SECRET_KEY` in `settings.py` is a development placeholder.
- Do not commit `db.sqlite3`, `node_modules/` or virtualenvs (already gitignored).

## Before opening a PR (review checklist)

1. `python manage.py check` and `python manage.py makemigrations --check --dry-run` are clean.
2. `CHANNEL_LAYER=memory python manage.py test` passes.
3. If you touched the frontend: `npm run build` succeeds.
4. If you changed behavior, a test covers it, and you ran the app and exercised the change (UI or `curl`).
5. The diff contains only what the PR description says.
