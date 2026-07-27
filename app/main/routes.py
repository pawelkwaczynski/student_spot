from __future__ import annotations

import json
import unicodedata
from pathlib import Path

from flask import Blueprint, current_app, g, render_template

from app.models import Club, Event, NewsPost, Notification, Reservation, Room, utcnow
from app.security import login_required

bp = Blueprint("main", __name__)


LOCAL_HERO_IMAGE_FILES = {
    "Adrian Makoć": "media/people/adrian-makoc.webp",
    "Aleksandra Świstak": "media/people/aleksandra-swistak.webp",
    "Anita Skorupska": "media/people/anita-skorupska.webp",
    "Anna Wichrowska": "media/people/anna-wichrowska.webp",
    "Artur Sendyka": "media/people/artur-sendyka.webp",
    "Bartłomiej Rosiak": "media/people/bartlomiej-rosiak.webp",
    "Błażej Strus": "media/people/blazej-strus.webp",
    "Damian Domański": "media/people/damian-domanski.webp",
    "Dawid Nielaba": "media/people/dawid-nielaba.webp",
    "Gabriela Kubacka": "media/people/gabriela-kubacka.webp",
    "Jarosław Grzesicki": "media/people/jaroslaw-grzesicki.webp",
    "Julia Czaja": "media/people/julia-czaja.webp",
    "Klaudia Dzieputa": "media/people/klaudia-dzieputa.webp",
    "Marcin Możdżan": "media/people/marcin-mozdzan.webp",
    "Marek Nowicki": "media/people/marek-nowicki.webp",
    "Mariuszu Nguyen": "media/people/mariusz-nguyen.webp",
    "Michał Ćwikliński": "media/people/michal-cwiklinski.webp",
    "Natalia Augustyniak": "media/people/natalia-augustyniak.webp",
    "Oliwia Tyralska": "media/people/oliwia-tyralska.webp",
    "Patrycja Pąśko": "media/people/patrycja-pasko.webp",
    "Patrycja Plich": "media/people/patrycja-plich.webp",
    "Sylwia Łongwa": "media/people/sylwia-longwa.webp",
    "Tomasz Ziółkowski": "media/people/tomasz-ziolkowski.webp",
}

LOCAL_HERO_NAME_OVERRIDES = {
    "Mariuszu Nguyen": "Mariusz Nguyen",
}

LOCAL_HERO_FEATURED_ORDER = {
    "Błażej Strus": 0,
}

CLUB_HERO_KEYWORDS = {
    "airon": ("informatyka", "technologie przetwarzania danych", "machine learning", "computer vision", "programowanie"),
    "grafika": ("grafika", "komunikacja wizualna", "game art", "multimedia", "projektowanie graficzne"),
    "kognitywistyczno-eksperymentalne": ("kognitywistyka", "neurodydaktyka", "psychologia", "fact-checking"),
    "progressus": ("zarządzanie", "ekonomia", "audyt", "biznes"),
    "wkreceni": ("kulturoznawstwo", "kultura", "menedżer kultury", "producent"),
    "warsztaty-emocji": ("arteterapia", "terapia pedagogiczna", "pedagogika"),
    "pedagogika-dziecka": ("pedagogika", "dydaktyka", "psychologia rozwoju"),
    "mlodzi-dziennikarze": ("dziennikarstwo", "komunikacja społeczna", "media"),
    "pielegniarstwo": ("pielęgniarstwo", "kosmetologia medyczna"),
    "europa-nostra": ("politologia", "administracja", "samorząd"),
    "mlody-samorzadowiec": ("politologia", "administracja", "samorząd"),
}


def normalize_text(value: str | None) -> str:
    normalized = unicodedata.normalize("NFKD", value or "").replace("ł", "l").replace("Ł", "L")
    return "".join(character for character in normalized if not unicodedata.combining(character)).casefold()


def local_hero_sort_key(hero: dict[str, str]) -> tuple[int, str]:
    return (LOCAL_HERO_FEATURED_ORDER.get(hero["name"], 1), normalize_text(hero["name"]))


def load_local_heroes() -> list[dict[str, str]]:
    source_path = Path(current_app.root_path).parent / "source_info" / "ahe-2026-06-15.json"
    if not source_path.exists():
        return []
    records = json.loads(source_path.read_text(encoding="utf-8"))
    heroes = []
    for record in records:
        raw_name = record.get("field-content", "").strip()
        image = LOCAL_HERO_IMAGE_FILES.get(raw_name)
        if not image:
            continue
        heroes.append(
            {
                "name": LOCAL_HERO_NAME_OVERRIDES.get(raw_name, raw_name),
                "program": record.get("field-content (2)", "").strip(),
                "bio": record.get("field-content (3)", "").strip(),
                "image": image,
            }
        )
    return sorted(heroes, key=local_hero_sort_key)


def primary_membership_for(user):
    approved = [membership for membership in user.memberships if membership.status == "approved"]
    pending = [membership for membership in user.memberships if membership.status == "pending"]
    memberships = approved or pending
    return sorted(memberships, key=lambda membership: membership.created_at or 0)[0] if memberships else None


def news_posts_for_club(club: Club | None) -> list[NewsPost]:
    if club is None:
        return []
    club_terms = [club.slug, club.name_pl, club.name_en, *club.tags]
    normalized_terms = [normalize_text(term) for term in club_terms if len(normalize_text(term)) > 2]
    posts = []
    for post in NewsPost.query.order_by(NewsPost.id.asc()).all():
        post_club = normalize_text(post.club)
        if any(post_club in term or term in post_club for term in normalized_terms):
            posts.append(post)
    return posts


def rooms_for_club(club: Club | None) -> list[Room]:
    if club is None:
        return []
    suggested = [normalize_text(room) for room in club.suggested_rooms]
    rooms = Room.query.filter_by(is_active=True).order_by(Room.name.asc(), Room.code.asc()).all()
    matched_rooms = []
    for room in rooms:
        room_terms = {normalize_text(room.code), normalize_text(room.name)}
        for wanted in suggested:
            is_training_room_alias = "szkoleniow" in wanted and room.code == "S01"
            if is_training_room_alias or wanted in room_terms or any(wanted in term or term in wanted for term in room_terms):
                matched_rooms.append(room)
                break
    return matched_rooms


def hero_keywords_for_club(club: Club) -> list[str]:
    explicit_keywords = CLUB_HERO_KEYWORDS.get(club.slug, ())
    fallback_keywords = [
        club.name_pl,
        club.name_en,
        *club.tags,
        *(major.name_pl for major in club.majors),
        *(major.name_en for major in club.majors),
    ]
    keywords = [normalize_text(keyword) for keyword in (*explicit_keywords, *fallback_keywords)]
    return sorted({keyword for keyword in keywords if len(keyword) > 3}, key=len, reverse=True)


def local_heroes_for_club(club: Club | None, limit: int = 3) -> list[dict[str, str]]:
    if club is None:
        return []
    keywords = hero_keywords_for_club(club)
    matches = []
    for hero in load_local_heroes():
        haystack = normalize_text(" ".join([hero["name"], hero["program"], hero["bio"]]))
        if any(keyword in haystack for keyword in keywords):
            matches.append(hero)
    return sorted(matches, key=local_hero_sort_key)[:limit]


@bp.route("/")
def index():
    clubs = Club.query.filter_by(is_public=True).order_by(Club.is_featured.desc(), Club.name_pl.asc()).limit(7).all()
    rooms = Room.query.filter_by(is_active=True).order_by(Room.name.asc(), Room.code.asc()).limit(4).all()
    events = Event.query.order_by(Event.starts_at.asc()).limit(4).all()
    posts = NewsPost.query.order_by(NewsPost.created_at.desc(), NewsPost.id.desc()).limit(3).all()
    return render_template("main/index.html", clubs=clubs, rooms=rooms, events=events, posts=posts)


@bp.route("/news")
def news():
    posts = NewsPost.query.order_by(NewsPost.created_at.desc(), NewsPost.id.desc()).all()
    return render_template("main/news.html", posts=posts)


@bp.route("/calendar")
def calendar():
    reservations = (
        Reservation.query.filter(
            Reservation.status.in_(("approved", "pending")),
            Reservation.ends_at >= utcnow(),
        )
        .order_by(Reservation.starts_at.asc())
        .limit(60)
        .all()
    )
    return render_template("main/calendar.html", reservations=reservations)


@bp.route("/local-heroes")
def local_heroes():
    return render_template("main/local_heroes.html", heroes=load_local_heroes())


@bp.route("/info")
def info():
    return render_template("main/info.html")


@bp.route("/media")
def media():
    return render_template("main/media.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    user = g.user
    memberships = user.memberships
    primary_membership = primary_membership_for(user)
    my_club = primary_membership.club if primary_membership else None
    club_ids = [membership.club_id for membership in memberships if membership.status == "approved"]
    next_event = (
        Event.query.filter(Event.club_id.in_(club_ids)).order_by(Event.starts_at.asc()).first()
        if club_ids
        else None
    )
    reservations = Reservation.query.filter_by(created_by_id=user.id).order_by(Reservation.created_at.desc()).limit(5).all()
    notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).limit(6).all()
    recommended_query = Club.query.filter_by(is_public=True)
    if user.major_id:
        recommended_query = recommended_query.filter(Club.majors.any(id=user.major_id))
    recommended_clubs = recommended_query.order_by(Club.is_featured.desc(), Club.name_pl.asc()).limit(4).all()
    if not recommended_clubs:
        recommended_clubs = Club.query.filter_by(is_public=True, is_featured=True).order_by(Club.name_pl.asc()).limit(4).all()
    return render_template(
        "main/dashboard.html",
        memberships=memberships,
        primary_membership=primary_membership,
        my_club=my_club,
        club_news=news_posts_for_club(my_club),
        club_rooms=rooms_for_club(my_club),
        club_heroes=local_heroes_for_club(my_club),
        next_event=next_event,
        reservations=reservations,
        notifications=notifications,
        recommended_clubs=recommended_clubs,
    )
