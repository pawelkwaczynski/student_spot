from __future__ import annotations

from flask import Blueprint, abort, flash, g, redirect, render_template, url_for

from app.extensions import db
from app.forms import ClubMessageForm
from app.models import Club, ClubMembership, ClubMessage, ClubMessageRecipient
from app.security import login_required
from app.services import audit, notify, user_can_manage_club

bp = Blueprint("messages", __name__)


def manageable_clubs_for(user):
    if user.global_role == "system_admin":
        return Club.query.order_by(Club.name_pl.asc()).all()
    if user.global_role == "club_guardian":
        return Club.query.filter_by(guardian_id=user.id).order_by(Club.name_pl.asc()).all()
    return []


def approved_members_for(club: Club):
    return (
        ClubMembership.query.filter_by(club_id=club.id, status="approved")
        .join(ClubMembership.user)
        .order_by(ClubMembership.created_at.asc())
        .all()
    )


@bp.route("/")
@login_required
def inbox():
    received = (
        ClubMessageRecipient.query.filter_by(recipient_id=g.user.id)
        .join(ClubMessageRecipient.message)
        .order_by(ClubMessage.created_at.desc())
        .all()
    )
    sent = []
    if manageable_clubs_for(g.user):
        sent = ClubMessage.query.filter_by(sender_id=g.user.id).order_by(ClubMessage.created_at.desc()).limit(8).all()
    return render_template("messages/inbox.html", received=received, sent=sent, manageable_clubs=manageable_clubs_for(g.user))


@bp.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    clubs = sorted(
        manageable_clubs_for(g.user),
        key=lambda club: (len(approved_members_for(club)) == 0, club.name_pl.casefold()),
    )
    if not clubs:
        abort(403)
    form = ClubMessageForm()
    form.club_id.choices = [(club.id, club.name_pl if g.locale == "pl" else club.name_en) for club in clubs]
    if form.validate_on_submit():
        club = db.session.get(Club, form.club_id.data)
        if club is None or not user_can_manage_club(g.user, club):
            abort(403)
        memberships = approved_members_for(club)
        if not memberships:
            flash("no_message_recipients", "warning")
            return render_template("messages/compose.html", form=form, recipient_count=0)
        message = ClubMessage(
            club=club,
            sender=g.user,
            subject=form.subject.data.strip(),
            body=form.body.data.strip(),
        )
        db.session.add(message)
        db.session.flush()
        for membership in memberships:
            db.session.add(ClubMessageRecipient(message=message, recipient=membership.user))
            notify(
                membership.user,
                f"Nowa wiadomość od opiekuna koła: {message.subject}",
                f"New message from the club guardian: {message.subject}",
            )
        audit("club_message_sent", user=g.user, object_type="club_message", object_id=message.id, count=len(memberships))
        db.session.commit()
        flash("club_message_sent", "success")
        return redirect(url_for("messages.inbox"))
    selected_club = clubs[0] if clubs else None
    return render_template(
        "messages/compose.html",
        form=form,
        recipient_count=len(approved_members_for(selected_club)) if selected_club else 0,
    )


@bp.route("/<int:recipient_id>")
@login_required
def detail(recipient_id: int):
    recipient = ClubMessageRecipient.query.get_or_404(recipient_id)
    if recipient.recipient_id != g.user.id and recipient.message.sender_id != g.user.id:
        abort(403)
    if recipient.recipient_id == g.user.id and recipient.read_at is None:
        from app.models import utcnow

        recipient.read_at = utcnow()
        db.session.commit()
    return render_template("messages/detail.html", item=recipient)
