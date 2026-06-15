from __future__ import annotations

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import or_

from app.extensions import db
from app.forms import ActivationForm, LoginForm, ProfileForm, RegistrationForm
from app.i18n import t
from app.models import Club, Major, User, utcnow
from app.security import hash_password, login_required, login_user, logout_user, verify_password
from app.services import activate_user_with_code, audit, avatar_upload_is_allowed, create_activation_token, save_user_avatar

bp = Blueprint("auth", __name__)


def generated_nickname_for(user_or_index) -> str:
    index_number = getattr(user_or_index, "index_number", user_or_index)
    if index_number:
        return f"student-{index_number}"
    user_id = getattr(user_or_index, "id", None)
    return f"user-{user_id}"


def is_generated_nickname(user: User) -> bool:
    return user.nickname in {generated_nickname_for(user), f"user-{user.id}"}


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    locale = session.get("lang", "pl")
    form.major_id.choices = [
        (major.id, major.name_pl if locale == "pl" else major.name_en)
        for major in Major.query.order_by(Major.name_pl).all()
    ]
    form.study_level.choices = [
        ("first_cycle", t("study_level_first_cycle")),
        ("second_cycle", t("study_level_second_cycle")),
        ("long_cycle", t("study_level_long_cycle")),
    ]
    form.study_mode.choices = [
        ("full_time", t("study_mode_full_time")),
        ("part_time", t("study_mode_part_time")),
        ("puw", t("study_mode_puw")),
    ]
    if form.validate_on_submit():
        nickname = (form.nickname.data or "").strip()
        if User.query.filter_by(index_number=form.index_number.data).first():
            form.index_number.errors.append("Index already exists.")
        if User.query.filter_by(email=form.email.data.lower()).first():
            form.email.errors.append("E-mail already exists.")
        if nickname and User.query.filter_by(nickname=nickname).first():
            form.nickname.errors.append("Nickname already exists.")
        if not form.errors:
            user = User(
                index_number=form.index_number.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                nickname=nickname or generated_nickname_for(form.index_number.data),
                email=form.email.data.lower(),
                password_hash=hash_password(form.password.data),
                year_of_study=form.year_of_study.data,
                major_id=form.major_id.data,
                study_level=form.study_level.data,
                study_mode=form.study_mode.data,
                global_role="student",
                account_status="pending_verification",
                preferred_language=session.get("lang", "pl"),
                terms_accepted_at=utcnow(),
                privacy_accepted_at=utcnow(),
            )
            db.session.add(user)
            db.session.flush()
            login_user(user)
            code = create_activation_token(user)
            audit("user_registered", user=user, object_type="user", object_id=user.id)
            db.session.commit()
            flash("activation_sent", "success")
            if code:
                flash(t("dev_activation_code", code=code), "info")
            return redirect(url_for("auth.activate"))
    return render_template("auth/register.html", form=form)


@bp.route("/activate", methods=["GET", "POST"])
def activate():
    form = ActivationForm()
    if form.validate_on_submit():
        user = g.get("user")
        if user and activate_user_with_code(user, form.code.data):
            db.session.commit()
            flash("account_activated", "success")
            return redirect(url_for("auth.choose_club"))
        flash("invalid_activation", "danger")
    return render_template("auth/activate.html", form=form, dev_code=session.get("dev_activation_code"))


@bp.route("/choose-club")
@login_required
def choose_club():
    user = g.user
    recommended_query = Club.query.filter_by(is_public=True)
    if user.major_id:
        recommended_query = recommended_query.filter(Club.majors.any(id=user.major_id))
    recommended_clubs = recommended_query.order_by(Club.is_featured.desc(), Club.name_pl.asc()).limit(6).all()
    if not recommended_clubs:
        recommended_clubs = Club.query.filter_by(is_public=True, is_featured=True).order_by(Club.name_pl.asc()).limit(6).all()
    return render_template("auth/choose_club.html", recommended_clubs=recommended_clubs)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_value = form.login.data.lower().strip()
        user = User.query.filter(or_(User.email == login_value, User.index_number == login_value)).first()
        if not user or not verify_password(user.password_hash, form.password.data):
            audit("login_failed", object_type="user")
            db.session.commit()
            flash("invalid_login", "danger")
            return render_template("auth/login.html", form=form), 401
        login_user(user)
        audit("login_success", user=user, object_type="user", object_id=user.id)
        db.session.commit()
        if not user.is_active:
            flash("inactive_account", "warning")
            return redirect(url_for("auth.activate"))
        return redirect(url_for("main.dashboard"))
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("logout", "info")
    return redirect(url_for("main.index"))


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=g.user)
    if request.method == "GET" and is_generated_nickname(g.user):
        form.nickname.data = ""
    if form.validate_on_submit():
        nickname = (form.nickname.data or "").strip()
        stored_nickname = nickname or generated_nickname_for(g.user)
        if User.query.filter(User.nickname == stored_nickname, User.id != g.user.id).first():
            form.nickname.errors.append("Nickname already exists.")
        password_change_requested = any(
            [
                form.current_password.data,
                form.new_password.data,
                form.confirm_new_password.data,
            ]
        )
        if password_change_requested:
            if not form.current_password.data:
                form.current_password.errors.append("Current password is required.")
            elif not verify_password(g.user.password_hash, form.current_password.data):
                form.current_password.errors.append("Current password is incorrect.")
            if not form.new_password.data:
                form.new_password.errors.append("New password is required.")
            if form.new_password.data != form.confirm_new_password.data:
                form.confirm_new_password.errors.append("Passwords must match.")
        avatar_file = form.avatar.data
        avatar_requested = bool(avatar_file and getattr(avatar_file, "filename", ""))
        if avatar_requested and not avatar_upload_is_allowed(avatar_file):
            form.avatar.errors.append("Allowed formats: PNG, JPG, JPEG, WEBP.")
        if form.errors:
            return render_template("auth/profile.html", form=form), 400
        else:
            g.user.first_name = form.first_name.data
            g.user.last_name = form.last_name.data
            g.user.nickname = stored_nickname
            g.user.preferred_language = form.preferred_language.data
            session["lang"] = form.preferred_language.data
            if password_change_requested and not form.errors:
                g.user.password_hash = hash_password(form.new_password.data)
            if avatar_requested:
                save_user_avatar(g.user, avatar_file)
            audit("profile_updated", user=g.user, object_type="user", object_id=g.user.id)
            db.session.commit()
            flash("profile_saved", "success")
            return redirect(url_for("auth.profile"))
    return render_template("auth/profile.html", form=form)
