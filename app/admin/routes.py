from __future__ import annotations

from datetime import date

from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from app.extensions import db
from app.forms import AdminDecisionForm
from app.models import AuditLog, Club, ClubMembership, Reservation, User
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
    membership = ClubMembership.query.get_or_404(membership_id)
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
    reservation = Reservation.query.get_or_404(reservation_id)
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
    club = Club.query.get_or_404(club_id)
    club.verification_status = "active_verified"
    club.last_verified_at = date.today()
    club.is_public = True
    audit("club_catalog_confirmed", user=g.user, object_type="club", object_id=club.id)
    db.session.commit()
    flash("club_confirmed", "success")
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
