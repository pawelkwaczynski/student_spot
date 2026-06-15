from __future__ import annotations

from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from sqlalchemy import case, or_

from app.extensions import db
from app.forms import MembershipRequestForm
from app.models import Club, ClubMembership, Major
from app.services import audit, notify

bp = Blueprint("clubs", __name__)


def can_view_hidden_club(club: Club) -> bool:
    user = g.get("user")
    if club.is_public:
        return True
    if not user:
        return False
    if user.global_role in {"system_admin", "property_admin"}:
        return True
    return user.global_role == "club_guardian" and club.guardian_id == user.id


@bp.route("")
@bp.route("/")
def list_clubs():
    query = Club.query.filter_by(is_public=True)
    search = (request.args.get("q") or "").strip()
    major_slug = (request.args.get("major") or "").strip()
    tag = (request.args.get("tag") or "").strip()
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Club.name_pl.ilike(pattern),
                Club.name_en.ilike(pattern),
                Club.description_pl.ilike(pattern),
                Club.description_en.ilike(pattern),
                Club.tags_csv.ilike(pattern),
            )
        )
    if major_slug:
        query = query.filter(Club.majors.any(Major.slug == major_slug))
    if tag:
        query = query.filter(Club.tags_csv.ilike(f"%{tag}%"))
    clubs = query.order_by(
        case((Club.slug == "pedagogika-dziecka", 1), else_=0),
        Club.is_featured.desc(),
        Club.name_pl.asc(),
    ).all()
    public_clubs = Club.query.filter_by(is_public=True).all()
    tags = sorted({item for club in public_clubs for item in club.tags}, key=str.lower)
    majors = Major.query.order_by(Major.name_pl.asc()).all()
    return render_template(
        "clubs/list.html",
        clubs=clubs,
        majors=majors,
        tags=tags,
        selected_major=major_slug,
        selected_tag=tag,
        search=search,
    )


@bp.route("/<int:club_id>", methods=["GET", "POST"])
def detail(club_id: int):
    club = Club.query.get_or_404(club_id)
    if not can_view_hidden_club(club):
        abort(404)
    if request.method == "POST" and not g.get("user"):
        flash("login_required", "warning")
        return redirect(url_for("auth.login"))
    form = MembershipRequestForm()
    form.club_id.data = str(club.id)
    existing = (
        ClubMembership.query.filter_by(user_id=g.user.id, club_id=club.id).first()
        if g.get("user")
        else None
    )
    if form.validate_on_submit():
        if existing:
            flash("membership_requested", "info")
            return redirect(url_for("clubs.detail", club_id=club.id))
        membership = ClubMembership(
            user=g.user,
            club=club,
            request_type=form.request_type.data,
            status="pending",
            club_role="member",
        )
        db.session.add(membership)
        if club.guardian:
            notify(
                club.guardian,
                f"Nowy wniosek członkowski: {club.name_pl}.",
                f"New membership request: {club.name_en}.",
            )
        audit("membership_requested", user=g.user, object_type="club", object_id=club.id)
        db.session.commit()
        flash("membership_requested", "success")
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        abort(400)
    return render_template("clubs/detail.html", club=club, form=form, existing=existing)
