# Flask 10-Line Auth (PLEX Pattern)

A drop-in **10-line Flask session auth core** + a clean modern PLEX-style UI demo you can reuse anywhere.

## Overview
This repo shows a practical auth baseline for small Flask apps:
- A tiny, reusable auth “core” you can copy into any project (`plex_auth.py`)
- A minimal, production-shaped login + signup flow (hashed passwords, safe redirects)
- A polished PLEX-style UI (no frameworks)

This supports the PLEX article: **“From Zero to Sign-In: A 10-Line Flask Auth Pattern You Can Reuse Anywhere”** (link placeholder).

## Features
- ✅ **10-line auth core**: `login_user`, `logout_user`, `current_uid`, `@login_required`
- ✅ Password hashing via Werkzeug (`generate_password_hash`, `check_password_hash`)
- ✅ SQLite demo DB (easy to replace with Postgres/MySQL)
- ✅ Safe `next=` redirect handling (prevents open redirects)
- ✅ Hardened session cookie defaults (HTTPOnly + SameSite; Secure optional)
- ✅ Minimal tests to prove the flow

## Project Structure
```text
flask-10-line-auth/
├── app.py                 # Flask app: routes + wiring
├── plex_auth.py           # 10-line reusable auth core + safe_next_url()
├── db.py                  # SQLite users table + create/verify helpers
├── requirements.txt       # Flask + Werkzeug
├── .env.example           # Example env vars (SECRET_KEY, AUTH_DB, etc.)
├── templates/             # PLEX-style pages (index/login/signup/forgot/me)
├── static/
│   ├── css/app.css        # PLEX styling tokens + panels/buttons/inputs
│   ├── js/app.js          # (optional; may be unused)
│   └── img/plex-mark.svg  # PLEX mark
├── tests/
│   └── test_auth_flow.py  # Basic flow tests
└── LICENSE
````

## How it works

1. **Signup** creates a user row with a hashed password and logs them in
2. **Login** verifies the hash and writes `uid` to session
3. **Protected routes** use `@login_required` to redirect to `/login` when not signed in
4. After login, users return to a **safe** relative `next=` URL

Auth state is just session:

* `session["uid"] = <user id>`

## Installation

Clone:

```bash
git clone git@github-dorian:dorian-sotpyrc/flask-10-line-auth.git
cd flask-10-line-auth
```

Install deps (pick one):

### Option A: user site-packages (no venv)

```bash
python3 -m pip install --user -r requirements.txt
```

### Option B: system-wide (quick, but global)

```bash
sudo python3 -m pip install -r requirements.txt
```

## Run (port 7059)

No code changes needed:

```bash
python3 -c "import app; app.app.run(host='0.0.0.0', port=7059, debug=True)"
```

Open:

* [http://127.0.0.1:7059/](http://127.0.0.1:7059/)

## Tests

```bash
python3 -m unittest -v
```

## Using the 10-line auth core in your own app

Copy `plex_auth.py` into your project and:

```python
from plex_auth import login_required

@app.get("/me")
@login_required
def me():
    return "ok"
```

## PLEX article & context

This repo is explained in more detail in the PLEX article:

* `/post/from-zero-to-sign-in-a-10-line-flask-auth-pattern` (placeholder)

## Roadmap / Extensions

* Add CSRF protection for forms
* Replace SQLite with Postgres + migrations
* Add password reset tokens + email send
* Add rate-limiting for login attempts
* Add “remember me” (rotating session IDs)

## SEO Keywords

flask authentication, session auth, login required decorator, minimal auth pattern, werkzeug password hashing, sqlite flask login, flask sign up page, secure redirects, plex ui

## License

MIT
