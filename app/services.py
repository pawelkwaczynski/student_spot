from __future__ import annotations

import hashlib
import json
import secrets
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable

from flask import current_app, has_request_context, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import (
    AuditLog,
    Club,
    ClubMembership,
    EmailVerificationToken,
    Event,
    Notification,
    Reservation,
    ReservationStatusHistory,
    Room,
    RoomFeature,
    utcnow,
)

ALLOWED_AVATAR_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def anonymize_ip(ip_address: str | None) -> str | None:
    if not ip_address:
        return None
    return hashlib.sha256(ip_address.encode("utf-8")).hexdigest()[:32]


def audit(action: str, user=None, object_type: str | None = None, object_id: object | None = None, **metadata) -> None:
    safe_metadata = {
        key: value for key, value in metadata.items() if key not in {"password", "token", "email", "first_name", "last_name"}
    }
    db.session.add(
        AuditLog(
            user_id=getattr(user, "id", None),
            action=action,
            object_type=object_type,
            object_id=str(object_id) if object_id is not None else None,
            ip_hash=anonymize_ip(request.remote_addr if has_request_context() else None),
            metadata_json=json.dumps(safe_metadata, ensure_ascii=False) if safe_metadata else None,
        )
    )


def notify(user, message_pl: str, message_en: str) -> None:
    db.session.add(Notification(user=user, message_pl=message_pl, message_en=message_en))


def avatar_relative_path_for_user(user) -> str | None:
    if not user or not getattr(user, "id", None):
        return None
    avatar_dir = Path(current_app.static_folder) / "media" / "avatars"
    for extension in sorted(ALLOWED_AVATAR_EXTENSIONS):
        path = avatar_dir / f"user-{user.id}.{extension}"
        if path.exists():
            return f"media/avatars/user-{user.id}.{extension}"
    return None


def avatar_upload_is_allowed(storage) -> bool:
    filename = secure_filename(storage.filename or "")
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return extension in ALLOWED_AVATAR_EXTENSIONS


def save_user_avatar(user, storage) -> bool:
    filename = secure_filename(storage.filename or "")
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if not avatar_upload_is_allowed(storage):
        return False
    avatar_dir = Path(current_app.static_folder) / "media" / "avatars"
    avatar_dir.mkdir(parents=True, exist_ok=True)
    for old_path in avatar_dir.glob(f"user-{user.id}.*"):
        if old_path.suffix.lstrip(".").lower() in ALLOWED_AVATAR_EXTENSIONS:
            old_path.unlink()
    storage.save(avatar_dir / f"user-{user.id}.{extension}")
    return True


class ConsoleEmailService:
    def send(self, to: str, subject: str, body: str) -> None:
        current_app.logger.info("ConsoleEmailService queued subject=%s", subject)


class SmtpEmailService:
    def send(self, to: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = current_app.config["MAIL_DEFAULT_SENDER"]
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)
        with smtplib.SMTP(current_app.config["MAIL_SERVER"], current_app.config["MAIL_PORT"], timeout=15) as smtp:
            if current_app.config["MAIL_USE_TLS"]:
                smtp.starttls()
            if current_app.config["MAIL_USERNAME"]:
                smtp.login(current_app.config["MAIL_USERNAME"], current_app.config["MAIL_PASSWORD"])
            smtp.send_message(message)


def email_service():
    if current_app.config.get("MAIL_SERVER"):
        return SmtpEmailService()
    return ConsoleEmailService()


def create_activation_token(user) -> str | None:
    code = f"{secrets.randbelow(1_000_000):06d}"
    token = EmailVerificationToken(
        user=user,
        token_hash=generate_password_hash(code),
        expires_at=utcnow() + timedelta(hours=24),
    )
    db.session.add(token)
    email_service().send(
        user.email,
        "StudentSpot activation",
        f"Your StudentSpot activation code is: {code}",
    )
    if current_app.config.get("SHOW_DEV_ACTIVATION_CODE"):
        session["dev_activation_code"] = code
        return code
    session.pop("dev_activation_code", None)
    return None


def activate_user_with_code(user, code: str) -> bool:
    tokens = EmailVerificationToken.query.filter_by(user_id=user.id, used_at=None).order_by(
        EmailVerificationToken.created_at.desc()
    )
    for token in tokens:
        if token.expires_at < utcnow():
            continue
        if check_password_hash(token.token_hash, code):
            token.used_at = utcnow()
            user.account_status = "active"
            user.email_verified_at = utcnow()
            notify(user, "Konto zostało aktywowane.", "Your account has been activated.")
            audit("account_activated", user=user, object_type="user", object_id=user.id)
            return True
    return False


def user_can_manage_club(user, club: Club) -> bool:
    if user.global_role == "system_admin":
        return True
    if user.global_role == "club_guardian" and club.guardian_id == user.id:
        return True
    return False


def user_can_reserve_for_club(user, club: Club) -> bool:
    if user.global_role in {"system_admin", "property_admin", "utw_organizer", "club_guardian"}:
        return True
    return ClubMembership.query.filter(
        ClubMembership.user_id == user.id,
        ClubMembership.club_id == club.id,
        ClubMembership.status == "approved",
        ClubMembership.club_role.in_(("chair", "vice_chair")),
    ).first() is not None


def has_room_conflict(room_id: int, starts_at: datetime, ends_at: datetime, ignore_reservation_id: int | None = None) -> bool:
    query = Reservation.query.filter(
        Reservation.room_id == room_id,
        Reservation.status.in_(("pending", "approved")),
        Reservation.starts_at < ends_at,
        Reservation.ends_at > starts_at,
    )
    if ignore_reservation_id:
        query = query.filter(Reservation.id != ignore_reservation_id)
    return db.session.query(query.exists()).scalar()


def room_has_features(room: Room, feature_codes: Iterable[str]) -> bool:
    room_codes = {feature.code for feature in room.features}
    return set(feature_codes).issubset(room_codes)


def search_rooms(
    starts_at: datetime | None = None,
    ends_at: datetime | None = None,
    participants: int | None = None,
    feature_codes: Iterable[str] = (),
    accessibility_codes: Iterable[str] = (),
) -> list[Room]:
    required_codes = set(feature_codes) | set(accessibility_codes)
    rooms = Room.query.filter_by(is_active=True).order_by(Room.name.asc(), Room.code.asc()).all()
    matches: list[Room] = []
    for room in rooms:
        if participants and room.capacity < participants:
            continue
        if starts_at and ends_at and has_room_conflict(room.id, starts_at, ends_at):
            continue
        if not room_has_features(room, required_codes):
            continue
        matches.append(room)
    if not participants:
        return sorted(matches, key=lambda r: (r.name, r.code))
    return sorted(matches, key=lambda r: (r.capacity - participants, -len(r.features), r.name))


def change_reservation_status(reservation: Reservation, new_status: str, user, note: str | None = None) -> None:
    old_status = reservation.status
    reservation.status = new_status
    if new_status == "rejected":
        reservation.rejection_reason = note
    db.session.add(
        ReservationStatusHistory(
            reservation=reservation,
            from_status=old_status,
            to_status=new_status,
            note=note,
            changed_by=user,
        )
    )
    notify(
        reservation.created_by,
        f"Status rezerwacji '{reservation.title}' zmieniono na {new_status}.",
        f"Reservation '{reservation.title}' status changed to {new_status}.",
    )
    if new_status == "approved" and reservation.event is None:
        db.session.add(
            Event(
                reservation=reservation,
                club=reservation.club,
                room=reservation.room,
                title=reservation.title,
                description=reservation.description,
                starts_at=reservation.starts_at,
                ends_at=reservation.ends_at,
                visibility="members",
                planned_participants=reservation.participants,
                accessibility_summary=reservation.accessibility_notes,
            )
        )
    audit("reservation_status_changed", user=user, object_type="reservation", object_id=reservation.id, status=new_status)


def set_membership_status(membership: ClubMembership, status: str, club_role: str, user) -> None:
    membership.status = status
    membership.club_role = club_role or membership.club_role
    membership.decided_by = user
    membership.decided_at = utcnow()
    notify(
        membership.user,
        f"Status członkostwa w {membership.club.name_pl}: {status}.",
        f"Membership status in {membership.club.name_en}: {status}.",
    )
    audit("membership_status_changed", user=user, object_type="club_membership", object_id=membership.id, status=status)


def features_by_codes(codes: Iterable[str]) -> list[RoomFeature]:
    clean_codes = [code for code in codes if code]
    if not clean_codes:
        return []
    return RoomFeature.query.filter(RoomFeature.code.in_(clean_codes)).all()
