from __future__ import annotations

import json
import unicodedata
from pathlib import Path

from flask import Blueprint, current_app, g, render_template

from app.models import Club, Event, Notification, Reservation, Room
from app.security import login_required

bp = Blueprint("main", __name__)


NEWS_POSTS = [
    {
        "slug": "rada-programowa-informatyki",
        "date_pl": "2 kwietnia 2026",
        "date_en": "2 April 2026",
        "title_pl": "Student koła w Radzie Programowej Informatyki",
        "title_en": "Club student in the Computer Science Programme Council",
        "club": "AIrON",
        "image": "media/news/student_council.png",
        "source_url": "https://airon.ahe.lodz.pl/news/student-kola-w-radzie-programowej-informatyki/",
        "excerpt_pl": "Dawid Tomaszewski z koła AIrON reprezentuje studentów w Radzie Programowej kierunku Informatyka. To przykład, jak aktywność koła może przekładać się na realny wpływ na program studiów i współpracę z otoczeniem branżowym.",
        "excerpt_en": "Dawid Tomaszewski from AIrON represents students in the Computer Science Programme Council. It shows how club activity can influence study programmes and industry-facing cooperation.",
    },
    {
        "slug": "roadmapa-airon",
        "date_pl": "28 marca 2026",
        "date_en": "28 March 2026",
        "title_pl": "Roadmapa rozwoju Koła Naukowego AIRON",
        "title_en": "AIrON development roadmap",
        "club": "AIrON",
        "image": "media/news/roadmap.png",
        "source_url": "https://airon.ahe.lodz.pl/news/roadmapa-rozwoju-kola-naukowego-airon/",
        "excerpt_pl": "Plan rozwoju koła obejmuje warsztaty, projekty AI, gry, hackathony, konferencje i budowanie partnerstw. W StudentSpot taki wpis działa jako templatka aktualności koła naukowego.",
        "excerpt_en": "The club roadmap covers workshops, AI projects, games, hackathons, conferences, and partnerships. In StudentSpot this works as a template news item for a student club.",
    },
    {
        "slug": "slovian-salvation",
        "date_pl": "28 marca 2026",
        "date_en": "28 March 2026",
        "title_pl": "Slovian Salvation na Poznań Game Arena 2025",
        "title_en": "Slovian Salvation at Poznan Game Arena 2025",
        "club": "AIrON",
        "image": "media/news/slovian_salvation.png",
        "source_url": "https://airon.ahe.lodz.pl/news/slovian-salvation-na-poznan-game-arena-2025/",
        "excerpt_pl": "Projekt gry Grzegorza Piechowskiego i Gabriela Gosika łączy słowiański folklor z psychologicznym horrorem. To dobry przykład aktualności projektowej, którą koło może promować w aplikacji.",
        "excerpt_en": "The game project by Grzegorz Piechowski and Gabriel Gosik blends Slavic folklore with psychological horror. It is a strong example of a project update a club can promote in the app.",
    },
    {
        "slug": "hackathon-fcp",
        "date_pl": "28 marca 2026",
        "date_en": "28 March 2026",
        "title_pl": "Studenci koła AIrON AHE na Hackathonie FCP",
        "title_en": "AIrON AHE students at the FCP Hackathon",
        "club": "AIrON",
        "image": "media/news/hackathon.png",
        "source_url": "https://airon.ahe.lodz.pl/news/studenci-kola-naukowego-airon-ahe-na-hackathonie-fcp/",
        "excerpt_pl": "Zespół stworzył portal do obsługi usług miejskich z modułem AI klasyfikującym opinie. Wpis pokazuje, jak aktualności mogą dokumentować proces, role w zespole i efekt wydarzenia.",
        "excerpt_en": "The team built a city services portal with an AI opinion-classification module. The post shows how news can document process, team roles, and event outcomes.",
    },
    {
        "slug": "google-education-summit",
        "date_pl": "2 kwietnia 2026",
        "date_en": "2 April 2026",
        "title_pl": "Google for Education Higher Education Summit",
        "title_en": "Google for Education Higher Education Summit",
        "club": "AIrON",
        "image": "media/news/google_event.png",
        "source_url": "https://airon.ahe.lodz.pl/news/google-for-education-higher-education-summit-nowa-rzeczywistosc-nowe-mozliwosci/",
        "excerpt_pl": "Zapowiedź udziału w wydarzeniu edukacyjnym pokazuje, że StudentSpot może wspierać komunikację przed konferencją, warsztatem albo wyjazdem koła.",
        "excerpt_en": "The event announcement shows how StudentSpot can support communication before a conference, workshop, or club trip.",
    },
    {
        "slug": "kognitywistyka-inauguracja",
        "date_pl": "12 kwietnia 2025",
        "date_en": "12 April 2025",
        "title_pl": "Inauguracja Kognitywistyczno-Eksperymentalnego Koła Naukowego",
        "title_en": "Launch of the Cognitive and Experimental Research Group",
        "club": "Kognitywistyka",
        "image": "media/news/kognitywistyka.png",
        "source_url": "https://www.ahe.lodz.pl/kognitywistyka/kolo-naukowe",
        "excerpt_pl": "Koło rozwija zainteresowania umysłem, poznaniem, badaniami eksperymentalnymi i neurodydaktyką. Wpis stanowi templatkę dla kół spoza informatyki.",
        "excerpt_en": "The group develops interests in mind, cognition, experimental research, and neurodidactics. This post is a template for clubs outside computer science.",
    },
]


CALENDAR_SLOTS = [
    {
        "date": "2026-06-16",
        "time": "09:00-10:30",
        "room": "Sala K320",
        "club": "AIrON",
        "title_pl": "Sprint projektowy AI",
        "title_en": "AI project sprint",
        "status": "approved",
    },
    {
        "date": "2026-06-18",
        "time": "12:00-14:00",
        "room": "Aula A03",
        "club": "Progressus",
        "title_pl": "Warsztat zarządzania projektem",
        "title_en": "Project management workshop",
        "status": "approved",
    },
    {
        "date": "2026-06-23",
        "time": "15:15-17:00",
        "room": "Sala K200A",
        "club": "Grafika",
        "title_pl": "Portfolio review",
        "title_en": "Portfolio review",
        "status": "pending",
    },
    {
        "date": "2026-06-25",
        "time": "10:00-11:30",
        "room": "Sala szkoleniowa Sterlinga",
        "club": "UTW AHE",
        "title_pl": "Spotkanie organizacyjne UTW",
        "title_en": "UTW organization meeting",
        "status": "approved",
    },
    {
        "date": "2026-07-02",
        "time": "13:00-15:00",
        "room": "Aula A01",
        "club": "Wkręceni",
        "title_pl": "Prelekcja o kulturze cyfrowej",
        "title_en": "Digital culture talk",
        "status": "approved",
    },
    {
        "date": "2026-07-07",
        "time": "16:00-18:00",
        "room": "Aula A02",
        "club": "Kognitywistyka",
        "title_pl": "Seminarium neurodydaktyczne",
        "title_en": "Neurodidactics seminar",
        "status": "pending",
    },
    {
        "date": "2026-07-15",
        "time": "09:30-12:00",
        "room": "Sala K320",
        "club": "AIrON",
        "title_pl": "Laboratorium aplikacji webowych",
        "title_en": "Web app lab",
        "status": "approved",
    },
    {
        "date": "2026-07-22",
        "time": "11:00-12:30",
        "room": "Sala szkoleniowa Sterlinga",
        "club": "Pedagogika Dziecka",
        "title_pl": "Spotkanie metodyczne",
        "title_en": "Teaching methods meeting",
        "status": "approved",
    },
]


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


def news_posts_for_club(club: Club | None) -> list[dict[str, str]]:
    if club is None:
        return []
    club_terms = [club.slug, club.name_pl, club.name_en, *club.tags]
    normalized_terms = [normalize_text(term) for term in club_terms if len(normalize_text(term)) > 2]
    posts = []
    for post in NEWS_POSTS:
        post_club = normalize_text(post["club"])
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
    return render_template("main/index.html", clubs=clubs, rooms=rooms, events=events, posts=NEWS_POSTS[:3])


@bp.route("/news")
def news():
    return render_template("main/news.html", posts=NEWS_POSTS)


@bp.route("/calendar")
def calendar():
    return render_template("main/calendar.html", slots=CALENDAR_SLOTS)


@bp.route("/local-heroes")
def local_heroes():
    return render_template("main/local_heroes.html", heroes=load_local_heroes())


@bp.route("/demo")
def demo():
    return render_template("main/demo.html")


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
