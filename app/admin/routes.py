from __future__ import annotations

from datetime import date

from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from app.extensions import db
from app.models import AuditLog, Club, ClubMembership, NewsPost, Reservation, User
from app.security import login_required
from app.services import audit, change_reservation_status, notify, set_membership_status, user_can_manage_club

bp = Blueprint("admin", __name__)


def is_admin_user(user) -> bool:
    return user.global_role in {"system_admin", "property_admin", "club_guardian"}


@bp.route("/")
@login_required
def dashboard():
    if not is_admin_user(g.user):
        abort(403)
    memberships_query = ClubMembership.query.filter_by(status="pending")
    if g.user.global_role == "club_guardian":
        memberships_query = memberships_query.join(ClubMembership.club).filter_by(guardian_id=g.user.id)
    elif g.user.global_role == "property_admin":
        memberships_query = memberships_query.filter(False)
    reservations_query = Reservation.query.filter_by(status="pending")
    if g.user.global_role == "club_guardian":
        reservations_query = reservations_query.filter(False)
    memberships = memberships_query.order_by(ClubMembership.created_at.asc()).all()
    member_directory_query = ClubMembership.query.join(ClubMembership.club)
    if g.user.global_role == "club_guardian":
        member_directory_query = member_directory_query.filter(Club.guardian_id == g.user.id)
    elif g.user.global_role != "system_admin":
        member_directory_query = member_directory_query.filter(False)
    member_directory = (
        member_directory_query.order_by(Club.name_pl.asc(), ClubMembership.status.asc(), ClubMembership.created_at.asc()).all()
    )
    reservations = reservations_query.order_by(Reservation.created_at.asc()).all()
    hidden_clubs = []
    if g.user.global_role in {"system_admin", "property_admin"}:
        hidden_clubs = Club.query.filter_by(is_public=False).order_by(Club.name_pl.asc()).all()
    audit_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(12).all()
    return render_template(
        "admin/dashboard.html",
        memberships=memberships,
        member_directory=member_directory,
        reservations=reservations,
        hidden_clubs=hidden_clubs,
        audit_logs=audit_logs,
    )


@bp.route("/memberships/<int:membership_id>/decision", methods=["POST"])
@login_required
def decide_membership(membership_id: int):
    membership = db.get_or_404(ClubMembership, membership_id)
    if not user_can_manage_club(g.user, membership.club):
        abort(403)
    action = request.form.get("action")
    role = request.form.get("club_role") or "member"
    if action == "approve":
        set_membership_status(membership, "approved", role, g.user)
    elif action == "reject":
        set_membership_status(membership, "rejected", "member", g.user)
    else:
        abort(400)
    db.session.commit()
    flash("membership_decided", "success")
    return redirect(url_for("admin.dashboard"))


@bp.route("/reservations/<int:reservation_id>/decision", methods=["POST"])
@login_required
def decide_reservation(reservation_id: int):
    if g.user.global_role not in {"system_admin", "property_admin"}:
        abort(403)
    reservation = db.get_or_404(Reservation, reservation_id)
    action = request.form.get("action")
    reason = (request.form.get("rejection_reason") or "").strip()
    if action == "approve":
        change_reservation_status(reservation, "approved", g.user)
    elif action == "reject":
        if not reason:
            flash("reason_required", "danger")
            return redirect(url_for("admin.dashboard"))
        change_reservation_status(reservation, "rejected", g.user, note=reason)
    else:
        abort(400)
    db.session.commit()
    flash("reservation_decided", "success")
    return redirect(url_for("admin.dashboard"))


@bp.route("/clubs/<int:club_id>/confirm", methods=["POST"])
@login_required
def confirm_club(club_id: int):
    if g.user.global_role not in {"system_admin", "property_admin"}:
        abort(403)
    club = db.get_or_404(Club, club_id)
    club.verification_status = "active_verified"
    club.last_verified_at = date.today()
    club.is_public = True
    audit("club_catalog_confirmed", user=g.user, object_type="club", object_id=club.id)
    db.session.commit()
    flash("club_confirmed", "success")
    return redirect(url_for("admin.dashboard"))


PL_GENITIVE_MONTHS = {
    1: "stycznia", 2: "lutego", 3: "marca", 4: "kwietnia", 5: "maja", 6: "czerwca",
    7: "lipca", 8: "sierpnia", 9: "września", 10: "października", 11: "listopada", 12: "grudnia",
}

EN_MONTHS = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December",
}


def news_slug(title: str) -> str:
    import re
    import unicodedata

    base = unicodedata.normalize("NFKD", title.replace("ł", "l").replace("Ł", "L"))
    base = base.encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")[:140] or "news"
    slug = base
    counter = 2
    while NewsPost.query.filter_by(slug=slug).first() is not None:
        slug = f"{base}-{counter}"
        counter += 1
    return slug


@bp.route("/news", methods=["POST"])
@login_required
def create_news():
    if g.user.global_role not in {"system_admin", "club_guardian"}:
        abort(403)
    fields = {name: (request.form.get(name) or "").strip() for name in
              ("club", "title_pl", "title_en", "excerpt_pl", "excerpt_en", "source_url")}
    if not all(fields[name] for name in ("club", "title_pl", "title_en", "excerpt_pl", "excerpt_en")):
        flash("news_form_incomplete", "danger")
        return redirect(url_for("admin.dashboard"))
    today = date.today()
    post = NewsPost(
        slug=news_slug(fields["title_pl"]),
        club=fields["club"],
        title_pl=fields["title_pl"],
        title_en=fields["title_en"],
        excerpt_pl=fields["excerpt_pl"],
        excerpt_en=fields["excerpt_en"],
        date_pl=f"{today.day} {PL_GENITIVE_MONTHS[today.month]} {today.year}",
        date_en=f"{today.day} {EN_MONTHS[today.month]} {today.year}",
        image=None,
        source_url=fields["source_url"] or None,
    )
    db.session.add(post)
    db.session.flush()
    audit("news_post_created", user=g.user, object_type="news_post", object_id=post.id)
    db.session.commit()
    flash("news_added", "success")
    return redirect(url_for("admin.dashboard"))


@bp.route("/utw-announcements", methods=["POST"])
@login_required
def send_utw_announcement():
    if g.user.global_role not in {"system_admin", "property_admin"}:
        abort(403)
    message = (request.form.get("message") or "").strip()
    if not message:
        flash("message_required", "danger")
        return redirect(url_for("admin.dashboard"))
    recipients = User.query.filter_by(global_role="utw_organizer", account_status="active").all()
    for recipient in recipients:
        notify(
            recipient,
            f"Komunikat do UTW: {message}",
            f"UTW admin message: {message}",
        )
    audit("utw_announcement_sent", user=g.user, object_type="utw", object_id="organizers", count=len(recipients))
    db.session.commit()
    flash("utw_announcement_sent", "success")
    return redirect(url_for("admin.dashboard"))
