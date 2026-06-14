from __future__ import annotations

from datetime import datetime, timedelta

from app.extensions import db


def utcnow() -> datetime:
    return datetime.utcnow()


club_major_links = db.Table(
    "club_major_links",
    db.Column("club_id", db.Integer, db.ForeignKey("clubs.id"), primary_key=True),
    db.Column("major_id", db.Integer, db.ForeignKey("majors.id"), primary_key=True),
)


room_feature_links = db.Table(
    "room_feature_links",
    db.Column("room_id", db.Integer, db.ForeignKey("rooms.id"), primary_key=True),
    db.Column("feature_id", db.Integer, db.ForeignKey("room_features.id"), primary_key=True),
)


reservation_required_features = db.Table(
    "reservation_required_features",
    db.Column("reservation_id", db.Integer, db.ForeignKey("reservations.id"), primary_key=True),
    db.Column("feature_id", db.Integer, db.ForeignKey("room_features.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    index_number = db.Column(db.String(6), unique=True, nullable=True, index=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    nickname = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    year_of_study = db.Column(db.Integer, nullable=True)
    major_id = db.Column(db.Integer, db.ForeignKey("majors.id"), nullable=True)
    study_level = db.Column(db.String(40), nullable=True)
    study_mode = db.Column(db.String(40), nullable=True)
    global_role = db.Column(db.String(40), nullable=False, default="student", index=True)
    account_status = db.Column(db.String(40), nullable=False, default="pending_verification", index=True)
    preferred_language = db.Column(db.String(2), nullable=False, default="pl")
    email_verified_at = db.Column(db.DateTime, nullable=True)
    terms_accepted_at = db.Column(db.DateTime, nullable=True)
    privacy_accepted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    major = db.relationship("Major", back_populates="users")
    memberships = db.relationship(
        "ClubMembership",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="ClubMembership.user_id",
    )
    notifications = db.relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    reservations = db.relationship("Reservation", back_populates="created_by")

    @property
    def is_active(self) -> bool:
        return self.account_status == "active"

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class EmailVerificationToken(db.Model):
    __tablename__ = "email_verification_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    token_hash = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False, default=lambda: utcnow() + timedelta(hours=24))
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    user = db.relationship("User")


class Major(db.Model):
    __tablename__ = "majors"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=True, index=True)
    name_pl = db.Column(db.String(160), nullable=False, unique=True)
    name_en = db.Column(db.String(160), nullable=False)
    dean_contact_pl = db.Column(db.String(255), nullable=True)
    dean_contact_en = db.Column(db.String(255), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    verification_status = db.Column(db.String(40), nullable=False, default="unverified")
    last_verified_at = db.Column(db.Date, nullable=True)

    users = db.relationship("User", back_populates="major")
    clubs = db.relationship("Club", secondary=club_major_links, back_populates="majors")


class Organization(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(40), nullable=False, default="club")
    name_pl = db.Column(db.String(180), nullable=False)
    name_en = db.Column(db.String(180), nullable=False)
    description_pl = db.Column(db.Text, nullable=True)
    description_en = db.Column(db.Text, nullable=True)

    club = db.relationship("Club", back_populates="organization", uselist=False)


class Club(db.Model):
    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    slug = db.Column(db.String(160), unique=True, nullable=True, index=True)
    name_pl = db.Column(db.String(180), nullable=False)
    name_en = db.Column(db.String(180), nullable=False)
    description_pl = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=False)
    campus = db.Column(db.String(80), nullable=False, default="lodz", index=True)
    guardian_name = db.Column(db.String(255), nullable=True)
    contact_email = db.Column(db.String(255), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    website_url = db.Column(db.String(500), nullable=True)
    tags_csv = db.Column(db.String(600), nullable=True)
    suggested_rooms_csv = db.Column(db.String(400), nullable=True)
    is_public = db.Column(db.Boolean, nullable=False, default=True, index=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=False, index=True)
    verification_status = db.Column(db.String(40), nullable=False, default="unverified")
    last_verified_at = db.Column(db.Date, nullable=True)

    organization = db.relationship("Organization", back_populates="club")
    guardian = db.relationship("User", foreign_keys=[guardian_id])
    majors = db.relationship("Major", secondary=club_major_links, back_populates="clubs")
    memberships = db.relationship("ClubMembership", back_populates="club", cascade="all, delete-orphan")
    reservations = db.relationship("Reservation", back_populates="club")
    events = db.relationship("Event", back_populates="club")

    @property
    def tags(self) -> list[str]:
        return [tag.strip() for tag in (self.tags_csv or "").split(",") if tag.strip()]

    @property
    def suggested_rooms(self) -> list[str]:
        return [room.strip() for room in (self.suggested_rooms_csv or "").split(",") if room.strip()]


class ClubMembership(db.Model):
    __tablename__ = "club_memberships"
    __table_args__ = (
        db.UniqueConstraint("user_id", "club_id", name="uq_user_club_membership"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False, index=True)
    status = db.Column(db.String(40), nullable=False, default="pending", index=True)
    request_type = db.Column(db.String(40), nullable=False, default="join")
    club_role = db.Column(db.String(40), nullable=False, default="member", index=True)
    decided_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    decided_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    user = db.relationship("User", foreign_keys=[user_id], back_populates="memberships")
    club = db.relationship("Club", back_populates="memberships")
    decided_by = db.relationship("User", foreign_keys=[decided_by_id])


class RoomFeature(db.Model):
    __tablename__ = "room_features"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False, unique=True, index=True)
    name_pl = db.Column(db.String(160), nullable=False)
    name_en = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(40), nullable=False, default="equipment")


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), nullable=False, unique=True, index=True)
    name = db.Column(db.String(160), nullable=False)
    building = db.Column(db.String(80), nullable=False)
    floor = db.Column(db.String(40), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, index=True)
    room_type = db.Column(db.String(80), nullable=False)
    description_pl = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=False)
    location_hint_pl = db.Column(db.String(255), nullable=True)
    location_hint_en = db.Column(db.String(255), nullable=True)
    map_url = db.Column(db.String(500), nullable=True)
    photo_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    source_type = db.Column(db.String(80), nullable=False, default="source")
    source_url = db.Column(db.String(500), nullable=True)
    verification_status = db.Column(db.String(40), nullable=False, default="unverified")
    last_verified_at = db.Column(db.Date, nullable=True)

    features = db.relationship("RoomFeature", secondary=room_feature_links, backref="rooms")
    reservations = db.relationship("Reservation", back_populates="room")
    unavailability = db.relationship("RoomUnavailability", back_populates="room")


class RoomUnavailability(db.Model):
    __tablename__ = "room_unavailability"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False, index=True)
    starts_at = db.Column(db.DateTime, nullable=False, index=True)
    ends_at = db.Column(db.DateTime, nullable=False, index=True)
    reason = db.Column(db.String(255), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    room = db.relationship("Room", back_populates="unavailability")
    created_by = db.relationship("User")


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False, index=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False, index=True)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.String(80), nullable=False, default="meeting")
    starts_at = db.Column(db.DateTime, nullable=False, index=True)
    ends_at = db.Column(db.DateTime, nullable=False, index=True)
    participants = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(40), nullable=False, default="pending", index=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    requires_step_free_access = db.Column(db.Boolean, nullable=False, default=False)
    requires_elevator = db.Column(db.Boolean, nullable=False, default=False)
    requires_induction_loop = db.Column(db.Boolean, nullable=False, default=False)
    requires_accessible_computer = db.Column(db.Boolean, nullable=False, default=False)
    accessibility_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    created_by = db.relationship("User", back_populates="reservations")
    club = db.relationship("Club", back_populates="reservations")
    room = db.relationship("Room", back_populates="reservations")
    required_features = db.relationship("RoomFeature", secondary=reservation_required_features)
    status_history = db.relationship(
        "ReservationStatusHistory",
        back_populates="reservation",
        cascade="all, delete-orphan",
        order_by="ReservationStatusHistory.created_at",
    )
    event = db.relationship("Event", back_populates="reservation", uselist=False)


class ReservationStatusHistory(db.Model):
    __tablename__ = "reservation_status_history"

    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.id"), nullable=False, index=True)
    from_status = db.Column(db.String(40), nullable=True)
    to_status = db.Column(db.String(40), nullable=False)
    note = db.Column(db.Text, nullable=True)
    changed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    reservation = db.relationship("Reservation", back_populates="status_history")
    changed_by = db.relationship("User")


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.id"), nullable=True, unique=True)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False, index=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=True)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starts_at = db.Column(db.DateTime, nullable=False, index=True)
    ends_at = db.Column(db.DateTime, nullable=False)
    visibility = db.Column(db.String(40), nullable=False, default="members")
    planned_participants = db.Column(db.Integer, nullable=False, default=0)
    accessibility_summary = db.Column(db.String(255), nullable=True)

    reservation = db.relationship("Reservation", back_populates="event")
    club = db.relationship("Club", back_populates="events")
    room = db.relationship("Room")


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    message_pl = db.Column(db.String(255), nullable=False)
    message_en = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    user = db.relationship("User", back_populates="notifications")


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    action = db.Column(db.String(120), nullable=False, index=True)
    object_type = db.Column(db.String(80), nullable=True)
    object_id = db.Column(db.String(80), nullable=True)
    ip_hash = db.Column(db.String(64), nullable=True)
    metadata_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow, index=True)

    user = db.relationship("User")
