from __future__ import annotations

from functools import wraps
from flask import session, redirect, url_for, request

# --- 10-line reusable core ---
login_user  = lambda uid: session.__setitem__("uid", int(uid))
logout_user = lambda: session.pop("uid", None)
current_uid = lambda: session.get("uid")

def login_required(view):
    @wraps(view)
    def wrapped(*a, **k):
        return view(*a, **k) if current_uid() else redirect(url_for("login", next=request.path))
    return wrapped
# ----------------------------

def safe_next_url(default: str = "/me") -> str:
    """Allow only relative paths to prevent open redirects."""
    nxt = request.args.get("next") or default
    if not nxt.startswith("/") or nxt.startswith("//"):
        return default
    return nxt
