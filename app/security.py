from __future__ import annotations

from functools import wraps
from typing import Callable, Iterable

from flask import abort, flash, g, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    return check_password_hash(password_hash, password)


def current_user():
    from app.models import User

    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, int(user_id))


def login_user(user) -> None:
    session.clear()
    session["user_id"] = user.id
    session["lang"] = user.preferred_language or "pl"


def logout_user() -> None:
    session.clear()


def login_required(view: Callable):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.get("user"):
            flash("login_required", "warning")
            return redirect(url_for("auth.login"))
        if not g.user.is_active:
            flash("activate_account_first", "warning")
            return redirect(url_for("auth.activate"))
        return view(*args, **kwargs)

    return wrapped


def role_required(roles: Iterable[str]):
    allowed = set(roles)

    def decorator(view: Callable):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = g.get("user")
            if not user:
                return redirect(url_for("auth.login"))
            if user.global_role not in allowed:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


def user_can_reserve(user) -> bool:
    if not user:
        return False
    if user.global_role in {"system_admin", "property_admin", "utw_organizer", "club_guardian"}:
        return True
    return any(
        membership.status == "approved" and membership.club_role in {"chair", "vice_chair"}
        for membership in user.memberships
    )
