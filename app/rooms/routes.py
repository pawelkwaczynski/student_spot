from __future__ import annotations

from datetime import datetime

from flask import Blueprint, render_template, request

from app.models import RoomFeature
from app.services import search_rooms

bp = Blueprint("rooms", __name__)


def parse_search_window():
    date_value = request.args.get("date")
    start_value = request.args.get("start_time")
    end_value = request.args.get("end_time")
    if not (date_value and start_value and end_value):
        return None, None
    try:
        return (
            datetime.fromisoformat(f"{date_value}T{start_value}"),
            datetime.fromisoformat(f"{date_value}T{end_value}"),
        )
    except ValueError:
        return None, None


@bp.route("")
@bp.route("/")
def list_rooms():
    starts_at, ends_at = parse_search_window()
    participants = request.args.get("participants", type=int)
    feature_codes = request.args.getlist("features")
    accessibility_codes = request.args.getlist("accessibility")
    rooms = search_rooms(starts_at, ends_at, participants, feature_codes, accessibility_codes)
    for room in rooms:
        if participants:
            seats_left = room.capacity - participants
            room.match_delta = seats_left
        else:
            room.match_delta = None
    features = RoomFeature.query.order_by(RoomFeature.category, RoomFeature.name_pl).all()
    return render_template(
        "rooms/list.html",
        rooms=rooms,
        features=features,
        starts_at=starts_at,
        ends_at=ends_at,
        participants=participants,
        selected_features=set(feature_codes),
        selected_accessibility=set(accessibility_codes),
    )
