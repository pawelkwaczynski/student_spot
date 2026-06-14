from __future__ import annotations

from datetime import datetime

from flask import Blueprint, Response, abort, flash, g, redirect, render_template, request, url_for

from app.extensions import db
from app.forms import ReservationForm
from app.models import Club, ClubMembership, Reservation, ReservationStatusHistory, Room, RoomFeature, User
from app.security import login_required
from app.services import audit, features_by_codes, has_room_conflict, notify, user_can_reserve_for_club

bp = Blueprint("reservations", __name__)


def reservable_clubs_for(user):
    if user.global_role in {"system_admin", "property_admin", "club_guardian", "utw_organizer"}:
        return Club.query.order_by(Club.name_pl).all()
    memberships = ClubMembership.query.filter(
        ClubMembership.user_id == user.id,
        ClubMembership.status == "approved",
        ClubMembership.club_role.in_(("chair", "vice_chair")),
    ).all()
    return [membership.club for membership in memberships]


def can_download_calendar(user, reservation: Reservation) -> bool:
    if reservation.status != "approved":
        return False
    if reservation.created_by_id == user.id:
        return True
    if user.global_role in {"system_admin", "property_admin"}:
        return True
    if user.global_role == "club_guardian" and reservation.club.guardian_id == user.id:
        return True
    return (
        ClubMembership.query.filter_by(
            user_id=user.id,
            club_id=reservation.club_id,
            status="approved",
        ).first()
        is not None
    )


def escape_ics(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def format_ics_datetime(value: datetime) -> str:
    return value.strftime("%Y%m%dT%H%M%S")


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    clubs = reservable_clubs_for(g.user)
    if not clubs:
        abort(403)
    rooms = Room.query.filter_by(is_active=True).order_by(Room.name).all()
    form = ReservationForm()
    form.club_id.choices = [(club.id, club.name_pl) for club in clubs]
    form.room_id.choices = [(room.id, f"{room.code} - {room.name}") for room in rooms]
    preselected_room = request.args.get("room_id", type=int)
    if preselected_room and request.method == "GET":
        form.room_id.data = preselected_room
    if form.validate_on_submit():
        club = db.session.get(Club, form.club_id.data)
        room = db.session.get(Room, form.room_id.data)
        if not club or not room or not user_can_reserve_for_club(g.user, club):
            abort(403)
        starts_at = datetime.combine(form.date.data, form.start_time.data)
        ends_at = datetime.combine(form.date.data, form.end_time.data)
        if ends_at <= starts_at:
            form.end_time.errors.append("End time must be later than start time.")
        if form.participants.data > room.capacity:
            form.participants.errors.append("Too many participants for this room.")
        required_codes = request.form.getlist("required_features")
        accessibility_required = []
        if form.requires_induction_loop.data:
            accessibility_required.append("induction_loop")
        if form.requires_accessible_computer.data:
            accessibility_required.append("accessible_computer")
        all_required_codes = list(set(required_codes + accessibility_required))
        room_codes = {feature.code for feature in room.features}
        missing = set(all_required_codes) - room_codes
        if missing:
            form.room_id.errors.append("Room does not meet all selected requirements.")
        if has_room_conflict(room.id, starts_at, ends_at):
            form.date.errors.append("Reservation conflict.")
            flash("reservation_conflict", "danger")
        if not form.errors:
            reservation = Reservation(
                created_by=g.user,
                club=club,
                room=room,
                title=form.title.data,
                description=form.description.data,
                event_type=form.event_type.data,
                starts_at=starts_at,
                ends_at=ends_at,
                participants=form.participants.data,
                status="pending",
                requires_step_free_access=form.requires_step_free_access.data,
                requires_elevator=form.requires_elevator.data,
                requires_induction_loop=form.requires_induction_loop.data,
                requires_accessible_computer=form.requires_accessible_computer.data,
                accessibility_notes=form.accessibility_notes.data,
            )
            reservation.required_features = features_by_codes(all_required_codes)
            db.session.add(reservation)
            db.session.flush()
            db.session.add(
                ReservationStatusHistory(
                    reservation=reservation,
                    from_status=None,
                    to_status="pending",
                    note="created",
                    changed_by=g.user,
                )
            )
            for admin in User.query.filter(User.global_role.in_(("property_admin", "system_admin"))).all():
                notify(admin, f"Nowa rezerwacja: {reservation.title}.", f"New reservation: {reservation.title}.")
            audit("reservation_created", user=g.user, object_type="reservation", object_id=reservation.id)
            db.session.commit()
            flash("reservation_created", "success")
            return redirect(url_for("main.dashboard"))
    features = RoomFeature.query.order_by(RoomFeature.category, RoomFeature.name_pl).all()
    return render_template("reservations/new.html", form=form, rooms=rooms, features=features)


@bp.route("/<int:reservation_id>")
@login_required
def detail(reservation_id: int):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.created_by_id != g.user.id and g.user.global_role not in {"system_admin", "property_admin"}:
        abort(403)
    return render_template("reservations/detail.html", reservation=reservation)


@bp.route("/<int:reservation_id>/calendar.ics")
@login_required
def calendar_ics(reservation_id: int):
    reservation = Reservation.query.get_or_404(reservation_id)
    if not can_download_calendar(g.user, reservation):
        abort(403)
    location = f"{reservation.room.name}, {reservation.room.address}"
    body = "\r\n".join(
        [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//StudentSpot//Student Club Calendar//PL",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "BEGIN:VEVENT",
            f"UID:studentspot-reservation-{reservation.id}@studentspot.local",
            f"DTSTAMP:{format_ics_datetime(datetime.utcnow())}",
            f"DTSTART:{format_ics_datetime(reservation.starts_at)}",
            f"DTEND:{format_ics_datetime(reservation.ends_at)}",
            f"SUMMARY:{escape_ics(reservation.title)}",
            f"DESCRIPTION:{escape_ics(reservation.description)}",
            f"LOCATION:{escape_ics(location)}",
            "END:VEVENT",
            "END:VCALENDAR",
            "",
        ]
    )
    filename = f"studentspot-{reservation.id}.ics"
    return Response(
        body,
        mimetype="text/calendar; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
