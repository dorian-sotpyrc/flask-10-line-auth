from __future__ import annotations

import os
import sqlite3
from typing import Optional

from flask import Flask, g, render_template, request, redirect, url_for, flash

import db as dbmod
from plex_auth import login_user, logout_user, current_uid, login_required, safe_next_url


def create_app(test_db_path: Optional[str] = None) -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me")
    app.config["DB_PATH"] = test_db_path or os.environ.get("AUTH_DB", "auth.db")

    # Cookie hardening (good defaults for most apps)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    if os.environ.get("COOKIE_SECURE", "0") == "1":
        app.config["SESSION_COOKIE_SECURE"] = True

    def conn() -> sqlite3.Connection:
        if "db_conn" not in g:
            g.db_conn = dbmod.connect(app.config["DB_PATH"])
            dbmod.init_db(g.db_conn)
        return g.db_conn

    @app.teardown_appcontext
    def _close_db(_exc):
        c = g.pop("db_conn", None)
        if c is not None:
            c.close()

    @app.get("/")
    def index():
        if current_uid():
            return redirect(url_for("me"))
        return render_template("index.html", title="Flask 10-Line Auth")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            pw = request.form.get("password", "")

            if not email or "@" not in email:
                flash("Enter a valid email.", "error")
                return render_template("signup.html", title="Sign up"), 400
            if len(pw) < 8:
                flash("Password must be at least 8 characters.", "error")
                return render_template("signup.html", title="Sign up"), 400

            try:
                uid = dbmod.create_user(conn(), email, pw)
            except sqlite3.IntegrityError:
                flash("That email is already registered. Try logging in.", "error")
                return render_template("signup.html", title="Sign up"), 400

            login_user(uid)
            return redirect(url_for("me"))

        return render_template("signup.html", title="Sign up")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            pw = request.form.get("password", "")

            uid = dbmod.verify_user(conn(), email, pw)
            if not uid:
                flash("Invalid email or password.", "error")
                return render_template("login.html", title="Log in"), 401

            login_user(uid)
            return redirect(safe_next_url())

        return render_template("login.html", title="Log in")

    @app.get("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/forgot", methods=["GET", "POST"])
    def forgot():
        # Safe placeholder: never reveal whether an account exists.
        if request.method == "POST":
            flash("If that email exists, you’ll receive a reset link shortly.", "ok")
            return redirect(url_for("login"))
        return render_template("forgot.html", title="Reset password")

    @app.get("/me")
    @login_required
    def me():
        u = dbmod.get_user_by_id(conn(), current_uid())
        return render_template("me.html", title="Account", user=u)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7059, debug=True)

