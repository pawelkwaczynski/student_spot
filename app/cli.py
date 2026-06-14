from __future__ import annotations

from datetime import date, datetime, timedelta

import click
from flask import Flask

from app.extensions import db
from app.models import (
    Club,
    ClubMembership,
    Event,
    Major,
    Notification,
    Organization,
    Reservation,
    ReservationStatusHistory,
    Room,
    RoomFeature,
    User,
)
from app.security import hash_password

DEMO_PASSWORD = "StudentSpot123!"

MAJOR_SOURCE_DATA = [
    ("informatyka", "Informatyka", "Computer Science", "https://www.ahe.lodz.pl/informatyka"),
    ("grafika", "Grafika", "Graphic Arts", "https://www.ahe.lodz.pl/grafika"),
    ("pedagogika", "Pedagogika", "Pedagogy", "https://www.ahe.lodz.pl/pedagogika"),
    ("kognitywistyka", "Kognitywistyka", "Cognitive Science", "https://www.ahe.lodz.pl/kognitywistyka"),
    ("zarzadzanie", "Zarządzanie", "Management", "https://www.ahe.lodz.pl/zarzadzanie"),
    ("ekonomia", "Ekonomia", "Economics", "https://www.ahe.lodz.pl/ekonomia"),
    ("kulturoznawstwo", "Kulturoznawstwo", "Cultural Studies", "https://www.ahe.lodz.pl/kulturoznawstwo"),
    (
        "pedagogika-przedszkolna-i-wczesnoszkolna",
        "Pedagogika przedszkolna i wczesnoszkolna",
        "Preschool and Early School Pedagogy",
        "https://www.ahe.lodz.pl/pedagogika-przedszkolna-i-wczesnoszkolna",
    ),
    ("psychologia", "Psychologia", "Psychology", "https://www.ahe.lodz.pl/psychologia"),
    ("pielegniarstwo", "Pielęgniarstwo", "Nursing", "https://www.ahe.lodz.pl/pielegniarstwo"),
    ("filologia-polska", "Filologia polska", "Polish Studies", "https://www.ahe.lodz.pl/filologia-polska"),
    (
        "dziennikarstwo-i-komunikacja-spoleczna",
        "Dziennikarstwo i komunikacja społeczna",
        "Journalism and Social Communication",
        "https://www.ahe.lodz.pl/dziennikarstwo",
    ),
    ("administracja", "Administracja", "Public Administration", "https://www.ahe.lodz.pl/administracja"),
]

CLUB_SOURCE_DATA = [
    {
        "slug": "airon",
        "name_pl": "Koło Naukowe AIrON",
        "name_en": "AIrON Student Research Group",
        "description_pl": "Koło skupia studentów informatyki zainteresowanych sztuczną inteligencją, programowaniem, tworzeniem aplikacji, API, bazami danych, UX oraz projektami zespołowymi.",
        "description_en": "A student research group for computer science students interested in artificial intelligence, software development, APIs, databases, user experience and team projects.",
        "major_slugs": ["informatyka"],
        "guardian_name": "mgr inż. Zoltan Farkas",
        "contact_email": None,
        "source_url": "https://www.ahe.lodz.pl/aktualnosci/studenci-kola-naukowego-airon-ahe-na-hackathonie-fcp",
        "website_url": "https://airon.ahe.lodz.pl/",
        "tags": ["AI", "programowanie", "API", "bazy danych", "UX", "hackathony"],
        "suggested_rooms": ["K320", "K200A"],
        "verification_status": "active_verified",
        "is_public": True,
        "is_featured": True,
    },
    {
        "slug": "kognitywistyczno-eksperymentalne",
        "name_pl": "Kognitywistyczno-Eksperymentalne Koło Naukowe",
        "name_en": "Cognitive and Experimental Research Group",
        "description_pl": "Koło rozwija zainteresowania badaniami nad umysłem, poznaniem i sztuczną inteligencją, wspiera inicjatywy badawcze, warsztaty, konferencje i spotkania naukowe.",
        "description_en": "An interdisciplinary research group focused on cognition, mind, experimental research, neurocognitive science and artificial intelligence.",
        "major_slugs": ["kognitywistyka"],
        "guardian_name": "dr Rafał Tryścień",
        "contact_email": None,
        "source_url": "https://www.ahe.lodz.pl/kognitywistyka/kolo-naukowe",
        "website_url": None,
        "tags": ["kognitywistyka", "neuronauka", "AI", "badania eksperymentalne"],
        "suggested_rooms": ["K200A", "Sale szkoleniowe"],
        "verification_status": "active_verified",
        "is_public": True,
        "is_featured": True,
    },
    {
        "slug": "grafika",
        "name_pl": "Koło Naukowe Grafika",
        "name_en": "Graphic Design Student Research Group",
        "description_pl": "Koło działa przy Wydziale Artystycznym, rozwija kreatywność, proces projektowy, grafikę tradycyjną i cyfrową, networking, wystawy oraz działania portfolio.",
        "description_en": "A creative research group for students interested in graphic design, visual arts, photography, animation, digital tools and exhibitions.",
        "major_slugs": ["grafika"],
        "guardian_name": "mgr Klaudia Gołojuch",
        "contact_email": "kngrafika.ahe@gmail.com",
        "source_url": "https://www.ahe.lodz.pl/grafika/kolo-naukowe-grafika",
        "website_url": None,
        "tags": ["grafika", "design", "fotografia", "animacja", "wystawy"],
        "suggested_rooms": ["K320", "K200A"],
        "verification_status": "active_verified",
        "is_public": True,
        "is_featured": True,
    },
    {
        "slug": "warsztaty-emocji",
        "name_pl": "Koło Arteterapeutyczne Warsztaty Emocji",
        "name_en": "Emotions Workshop Art Therapy Group",
        "description_pl": "Koło organizuje warsztaty i projekty arteterapeutyczne, integruje środowisko studenckie, rozwija kreatywność oraz wspiera działalność publikacyjną.",
        "description_en": "An art therapy group using creative activities to support student development, integration, reflection and project work.",
        "major_slugs": ["pedagogika"],
        "guardian_name": "mgr Agnieszka Wójcik",
        "contact_email": "awojcik@ahe.email",
        "source_url": "https://www.ahe.lodz.pl/pedagogika/kola-naukowe/kolo-arteterapeutyczne",
        "website_url": None,
        "tags": ["arteterapia", "pedagogika", "sztuka", "emocje", "warsztaty"],
        "suggested_rooms": ["K005", "Sale szkoleniowe"],
        "verification_status": "active_verified",
        "is_public": True,
        "is_featured": True,
    },
    {
        "slug": "progressus",
        "name_pl": "Koło Naukowe Progressus",
        "name_en": "Progressus Student Research Group",
        "description_pl": "Koło przy Wydziale Ekonomii i Zarządzania wspiera projekty badawcze, konferencje, warsztaty edukacyjne, wyjazdy technologiczne i kontakty z biznesem.",
        "description_en": "A management and economics student group focused on practical projects, research, conferences, business relations and technology visits.",
        "major_slugs": ["zarzadzanie", "ekonomia"],
        "guardian_name": "mgr Anna Bojanowska-Sosnowska",
        "contact_email": "progressus@ahe.lodz.pl",
        "source_url": "https://www.ahe.lodz.pl/zarzadzanie/kolo-naukowe-progressus",
        "website_url": None,
        "tags": ["zarządzanie", "ekonomia", "biznes", "projekty", "konferencje"],
        "suggested_rooms": ["Aula A01", "K200A"],
        "verification_status": "active_verified",
        "is_public": True,
        "is_featured": True,
    },
    {
        "slug": "wkreceni",
        "name_pl": "Studenckie Koło Naukowe Miłośników Kultury Wkręceni",
        "name_en": "Wkręceni Cultural Studies Group",
        "description_pl": "Koło zrzesza studentów zainteresowanych kulturą i zarządzaniem kulturą, organizuje prelekcje, wspiera konferencje, publikacje oraz wydarzenia badawcze i kulturalne.",
        "description_en": "A cultural studies group supporting lectures, cultural events, research projects, academic publications and conference participation.",
        "major_slugs": ["kulturoznawstwo"],
        "guardian_name": "dr Katarzyna Filutowska; mgr Monika Kamieńska",
        "contact_email": "katarzyna.filutowska@ahe.email",
        "source_url": "https://www.ahe.lodz.pl/kulturoznawstwo/kola-naukowe/kolo-wkreceni",
        "website_url": None,
        "tags": ["kultura", "sztuka", "teatr", "gry", "AI", "wydarzenia"],
        "suggested_rooms": ["Aula A01", "Aula A03"],
        "verification_status": "active_verified",
        "is_public": True,
        "is_featured": True,
    },
    {
        "slug": "pedagogika-dziecka",
        "name_pl": "Koło Naukowe Pedagogiki Dziecka",
        "name_en": "Child Education Research Group",
        "description_pl": "Koło rozwija życie naukowe oraz wiedzę z zakresu pedagogiki przedszkolnej i wczesnoszkolnej, dydaktyki i psychologii rozwoju dziecka.",
        "description_en": "A child education research group focused on preschool and early school pedagogy, teaching methods, developmental psychology and educational research.",
        "major_slugs": ["pedagogika-przedszkolna-i-wczesnoszkolna"],
        "guardian_name": "dr Daria Modrzejewska",
        "contact_email": "dmodrzejewska@ahe.lodz.pl",
        "source_url": "https://www.ahe.lodz.pl/pedagogika-przedszkolna-i-wczesnoszkolna/kola-naukowe/kolo-naukowo-metodyczne",
        "website_url": None,
        "tags": ["pedagogika dziecka", "edukacja", "dydaktyka", "psychologia rozwoju"],
        "suggested_rooms": ["Sale szkoleniowe", "K200A"],
        "verification_status": "active_verified",
        "is_public": True,
        "is_featured": True,
    },
    {
        "slug": "moja-psychologia",
        "name_pl": "Koło Naukowe Moja Psychologia",
        "name_en": "My Psychology Student Research Group",
        "description_pl": "Oficjalna strona opisuje dyskusje, webinary, projekty badawcze, konferencje, szkolenia, warsztaty i seminaria; wymaga potwierdzenia aktualności.",
        "description_en": "A psychology student group offering discussions, webinars, research projects, workshops, seminars and conference activities; current activity needs confirmation.",
        "major_slugs": ["psychologia"],
        "guardian_name": "dr Joanna Paul-Kańska",
        "contact_email": "jpaul@ahe.lodz.pl",
        "source_url": "https://www.ahe.lodz.pl/psychologia/kolo-naukowe-moja-psychologia",
        "website_url": None,
        "tags": ["psychologia", "badania", "webinary", "warsztaty"],
        "suggested_rooms": ["Sale szkoleniowe"],
        "verification_status": "official_needs_verification",
        "is_public": False,
        "is_featured": False,
    },
    {
        "slug": "pielegniarstwo",
        "name_pl": "Studenckie Koło Naukowe Pielęgniarstwa",
        "name_en": "Nursing Student Research Group",
        "description_pl": "Koło służy poszerzaniu wiedzy z zakresu współczesnego pielęgniarstwa, interdyscyplinarnej praktyki, pisania prac i wystąpień konferencyjnych.",
        "description_en": "A nursing research group focused on contemporary nursing, interdisciplinary practice, scientific writing and conference participation.",
        "major_slugs": ["pielegniarstwo"],
        "guardian_name": "mgr Aleksandra Zdrojewska",
        "contact_email": None,
        "source_url": "https://www.ahe.lodz.pl/pielegniarstwo/kola-naukowe",
        "website_url": None,
        "tags": ["pielęgniarstwo", "medycyna", "badania", "konferencje"],
        "suggested_rooms": ["Sale szkoleniowe"],
        "verification_status": "official_needs_verification",
        "is_public": False,
        "is_featured": False,
    },
    {
        "slug": "profilowanie-kryminalistyczne",
        "name_pl": "Studenckie Koło Naukowe Profilowania Kryminalistycznego",
        "name_en": "Criminal Profiling Student Research Group",
        "description_pl": "Koło łączy filologię polską, psychologię postaci i profilowanie kryminalistyczne, analizując motywy działania i budowę wiarygodnych fabuł.",
        "description_en": "A Polish studies research group combining criminal profiling, character psychology and narrative construction.",
        "major_slugs": ["filologia-polska"],
        "guardian_name": "mgr Justyna Wolter; dr Natalia Piórczyńska-Krawczyńska",
        "contact_email": None,
        "source_url": "https://www.ahe.lodz.pl/filologia-polska/kola-naukowe",
        "website_url": None,
        "tags": ["profilowanie", "kryminologia", "psychologia postaci", "literatura"],
        "suggested_rooms": ["Sale szkoleniowe"],
        "verification_status": "official_needs_verification",
        "is_public": False,
        "is_featured": False,
    },
    {
        "slug": "mlodzi-dziennikarze",
        "name_pl": "Koło Naukowe Młodych Dziennikarzy",
        "name_en": "Young Journalists Student Research Group",
        "description_pl": "Interdyscyplinarne koło studentów dziennikarstwa i filologii polskiej związane z pracą redakcyjną, pisaniem i mediami studenckimi.",
        "description_en": "A journalism and Polish studies student group focused on editorial work, writing, reporting and student media.",
        "major_slugs": ["dziennikarstwo-i-komunikacja-spoleczna", "filologia-polska"],
        "guardian_name": None,
        "contact_email": None,
        "source_url": "https://www.ahe.lodz.pl/dziennikarstwo/kola-naukowe",
        "website_url": None,
        "tags": ["dziennikarstwo", "media", "redakcja", "artykuły"],
        "suggested_rooms": ["Sale szkoleniowe"],
        "verification_status": "official_needs_verification",
        "is_public": False,
        "is_featured": False,
    },
    {
        "slug": "europa-nostra",
        "name_pl": "Koło Naukowe Studentów Administracji Europa Nostra",
        "name_en": "Europa Nostra Public Administration Group",
        "description_pl": "Koło rozwija zainteresowania prawem i administracją, konferencjami, inicjatywami studenckimi, integracją i rozwojem zawodowym.",
        "description_en": "A public administration student group focused on administrative law, conferences, student initiatives and professional development.",
        "major_slugs": ["administracja"],
        "guardian_name": "mgr Mariusz Olężałek",
        "contact_email": None,
        "source_url": "https://www.ahe.lodz.pl/administracja/kola_naukowe",
        "website_url": None,
        "tags": ["administracja", "prawo", "samorząd", "konferencje"],
        "suggested_rooms": ["Sale szkoleniowe"],
        "verification_status": "official_needs_verification",
        "is_public": False,
        "is_featured": False,
    },
    {
        "slug": "mlody-samorzadowiec",
        "name_pl": "Studenckie Koło Naukowe Młodego Samorządowca",
        "name_en": "Young Local Government Student Research Group",
        "description_pl": "Koło rozwija praktyczną wiedzę z administracji samorządowej, świadomość prawną, politykę lokalną, badania i pracę grupową.",
        "description_en": "A local government and public administration group focused on legal awareness, local policy, research and teamwork.",
        "major_slugs": ["administracja"],
        "guardian_name": None,
        "contact_email": None,
        "source_url": "https://www.ahe.lodz.pl/administracja/kola_naukowe",
        "website_url": None,
        "tags": ["samorząd", "administracja", "prawo", "polityka lokalna"],
        "suggested_rooms": ["Sale szkoleniowe"],
        "verification_status": "official_needs_verification",
        "is_public": False,
        "is_featured": False,
    },
]


def register_cli(app: Flask) -> None:
    @app.cli.command("init-db")
    @click.option("--reset", is_flag=True, help="Drop all tables before creating them.")
    def init_db(reset: bool) -> None:
        if reset:
            db.drop_all()
        db.create_all()
        click.echo("Database schema ready.")

    @app.cli.command("seed-demo")
    def seed_demo_command() -> None:
        seed_demo()
        click.echo("Demo data seeded.")


def get_or_create(model, defaults: dict | None = None, **lookup):
    instance = model.query.filter_by(**lookup).first()
    if instance:
        return instance
    params = dict(defaults or {})
    params.update(lookup)
    instance = model(**params)
    db.session.add(instance)
    db.session.flush()
    return instance


def seed_demo() -> None:
    db.create_all()
    source_date = date(2026, 6, 14)
    password_hash = hash_password(DEMO_PASSWORD)

    majors = seed_majors(source_date)
    majors["informatics"] = majors["informatyka"]
    majors["graphics"] = majors["grafika"]
    majors["pedagogy"] = majors["pedagogika"]
    majors["cognitive"] = majors["kognitywistyka"]
    majors["management"] = majors["zarzadzanie"]

    users = {
        "admin": get_or_create(
            User,
            email="admin@studentspot.example.com",
            defaults={
                "index_number": None,
                "first_name": "Demo",
                "last_name": "Admin",
                "nickname": "admin",
                "password_hash": password_hash,
                "global_role": "system_admin",
                "account_status": "active",
                "preferred_language": "pl",
            },
        ),
        "property": get_or_create(
            User,
            email="property@studentspot.example.com",
            defaults={
                "first_name": "Demo",
                "last_name": "Property",
                "nickname": "property-admin",
                "password_hash": password_hash,
                "global_role": "property_admin",
                "account_status": "active",
                "preferred_language": "pl",
            },
        ),
        "guardian": get_or_create(
            User,
            email="guardian@studentspot.example.com",
            defaults={
                "first_name": "Demo",
                "last_name": "Guardian",
                "nickname": "guardian",
                "password_hash": password_hash,
                "global_role": "club_guardian",
                "account_status": "active",
                "preferred_language": "pl",
            },
        ),
        "boss": get_or_create(
            User,
            email="boss@studentspot.example.com",
            defaults={
                "index_number": "165318",
                "first_name": "Demo",
                "last_name": "Boss",
                "nickname": "boss",
                "password_hash": password_hash,
                "year_of_study": 2,
                "major": majors["informatics"],
                "global_role": "student",
                "account_status": "active",
                "preferred_language": "en",
            },
        ),
        "vice": get_or_create(
            User,
            email="vice@studentspot.example.com",
            defaults={
                "index_number": "165319",
                "first_name": "Demo",
                "last_name": "Vice",
                "nickname": "vice",
                "password_hash": password_hash,
                "year_of_study": 2,
                "major": majors["informatics"],
                "global_role": "student",
                "account_status": "active",
                "preferred_language": "pl",
            },
        ),
        "member": get_or_create(
            User,
            email="member@studentspot.example.com",
            defaults={
                "index_number": "165320",
                "first_name": "Demo",
                "last_name": "Member",
                "nickname": "member",
                "password_hash": password_hash,
                "year_of_study": 1,
                "major": majors["graphics"],
                "global_role": "student",
                "account_status": "active",
                "preferred_language": "pl",
            },
        ),
        "pending": get_or_create(
            User,
            email="pending@studentspot.example.com",
            defaults={
                "index_number": "165321",
                "first_name": "Demo",
                "last_name": "Pending",
                "nickname": "pending",
                "password_hash": password_hash,
                "year_of_study": 1,
                "major": majors["pedagogy"],
                "global_role": "student",
                "account_status": "active",
                "preferred_language": "pl",
            },
        ),
        "utw": get_or_create(
            User,
            email="utw@studentspot.example.com",
            defaults={
                "first_name": "Demo",
                "last_name": "UTW",
                "nickname": "utw",
                "password_hash": password_hash,
                "global_role": "utw_organizer",
                "account_status": "active",
                "preferred_language": "pl",
            },
        ),
    }

    for key in ("boss", "vice", "member", "pending"):
        users[key].study_level = users[key].study_level or "first_cycle"
        users[key].study_mode = users[key].study_mode or "part_time"
    for user in users.values():
        if user.account_status == "active" and not user.email_verified_at:
            user.email_verified_at = datetime(2026, 6, 14, 12, 0)
        if user.account_status == "active" and not user.terms_accepted_at and user.index_number:
            user.terms_accepted_at = datetime(2026, 6, 14, 12, 0)
            user.privacy_accepted_at = datetime(2026, 6, 14, 12, 0)

    features = {
        "projector": feature("projector", "Projektor", "Projector"),
        "screen": feature("screen", "Ekran", "Screen"),
        "sound": feature("sound", "Nagłośnienie", "Sound system"),
        "microphone": feature("microphone", "Mikrofon", "Microphone"),
        "computers": feature("computers", "Komputery", "Computers"),
        "wifi": feature("wifi", "Wi-Fi", "Wi-Fi"),
        "whiteboard": feature("whiteboard", "Tablica", "Whiteboard"),
        "flipchart": feature("flipchart", "Flipchart", "Flipchart"),
        "air_conditioning": feature("air_conditioning", "Klimatyzacja", "Air conditioning"),
        "stage": feature("stage", "Scena / podest", "Stage"),
        "induction_loop": feature("induction_loop", "Pętla indukcyjna", "Induction loop", "accessibility"),
        "elevator": feature("elevator", "Dostęp windą", "Elevator access", "accessibility"),
        "step_free": feature("step_free", "Bezstopniowy dostęp", "Step-free access", "accessibility"),
        "accessible_toilet": feature("accessible_toilet", "Toaleta dostępna", "Accessible toilet", "accessibility"),
        "wide_passages": feature("wide_passages", "Szerokie przejścia", "Wide passages", "accessibility"),
        "accessible_computer": feature(
            "accessible_computer",
            "Dostosowane stanowisko komputerowe",
            "Accessible computer station",
            "accessibility",
        ),
    }

    clubs = seed_clubs(users["guardian"], majors, source_date)

    membership(users["boss"], clubs["airon"], "approved", "chair")
    membership(users["vice"], clubs["airon"], "approved", "vice_chair")
    membership(users["member"], clubs["grafika"], "approved", "member")
    membership(users["pending"], clubs["warsztaty-emocji"], "pending", "member")

    rooms = {
        "A01": room(
            "A01",
            "Aula A01",
            "K",
            "Sterlinga 26",
            47,
            "aula",
            "Kameralna aula do spotkań i prezentacji. Szczegółowe wyposażenie wymaga potwierdzenia.",
            "Small lecture hall for meetings and presentations. Detailed equipment requires confirmation.",
            [features["projector"], features["screen"], features["wifi"], features["step_free"], features["elevator"]],
            "https://www.mojekonferencje.pl/lodz/akademia-humanistyczno-ekonomiczna-w-lodzi",
            "unverified",
            photo_url="media/rooms/aula-a01.webp",
        ),
        "A02": room(
            "A02",
            "Aula A02",
            "K",
            "Sterlinga 26",
            138,
            "aula",
            "Aula z projektorem i układem do większych prezentacji.",
            "Lecture hall with a projector and layout for larger presentations.",
            [
                features["projector"],
                features["screen"],
                features["wifi"],
                features["air_conditioning"],
                features["stage"],
                features["step_free"],
                features["elevator"],
            ],
            "https://www.konferencje.pl/o/akademia-humanistyczno-ekonomiczna-w-lodzi.html",
            "verified",
            photo_url="media/rooms/aula-a02.webp",
        ),
        "A03": room(
            "A03",
            "Aula A03",
            "K",
            "Sterlinga 26",
            73,
            "aula",
            "Aula z potwierdzoną klimatyzacją, Wi-Fi i projektorem.",
            "Lecture hall with confirmed air conditioning, Wi-Fi, and projector.",
            [
                features["projector"],
                features["screen"],
                features["sound"],
                features["wifi"],
                features["air_conditioning"],
                features["whiteboard"],
                features["flipchart"],
                features["step_free"],
                features["elevator"],
            ],
            "https://www.konferencje.pl/o/akademia-humanistyczno-ekonomiczna-w-lodzi/28883-aula-a03.html",
            "verified",
            photo_url="media/rooms/aula-a03.webp",
        ),
        "A04": room(
            "A04",
            "Aula A04",
            "K",
            "Sterlinga 26",
            84,
            "aula",
            "Aula do wykładów i spotkań. Pozostałe wyposażenie niepotwierdzone.",
            "Lecture hall for classes and meetings. Remaining equipment is unverified.",
            [features["projector"], features["wifi"], features["step_free"], features["elevator"]],
            "https://www.mojekonferencje.pl/lodz/akademia-humanistyczno-ekonomiczna-w-lodzi",
            "unverified",
            photo_url="media/rooms/aula-a04.webp",
        ),
        "K320": room(
            "K320",
            "Sala K320",
            "K",
            "Sterlinga 26",
            35,
            "computer_lab",
            "Robocza sala komputerowa dla warsztatów informatycznych i graficznych.",
            "Working computer room for IT and graphic workshops.",
            [features["computers"], features["projector"], features["wifi"], features["elevator"]],
            None,
            "unverified",
            floor="II",
            photo_url="media/rooms/computer-lab.avif",
        ),
        "K200A": room(
            "K200A",
            "Sala K200A",
            "K",
            "Sterlinga 26",
            45,
            "computer_lab",
            "Przestronniejsza robocza sala komputerowa do warsztatów.",
            "Larger working computer room for workshops.",
            [features["computers"], features["projector"], features["wifi"], features["elevator"]],
            None,
            "unverified",
            floor="II",
            photo_url="media/rooms/computer-lab.avif",
        ),
        "S01": room(
            "S01",
            "Sala szkoleniowa Sterlinga",
            "K",
            "Sterlinga 26",
            30,
            "training_room",
            "Sala szkoleniowa do mniejszych spotkań, warsztatów i konsultacji.",
            "Training room for smaller meetings, workshops, and consultations.",
            [features["projector"], features["screen"], features["wifi"], features["whiteboard"], features["step_free"], features["elevator"]],
            "https://www.mojekonferencje.pl/lodz/akademia-humanistyczno-ekonomiczna-w-lodzi",
            "unverified",
            photo_url="media/rooms/sale-szkoleniowe.webp",
        ),
    }

    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    create_reservation(
        users["vice"],
        clubs["airon"],
        rooms["A03"],
        "Warsztat AIrON",
        "Spotkanie warsztatowe koła AIrON z analizą danych.",
        now + timedelta(days=4, hours=2),
        now + timedelta(days=4, hours=4),
        35,
        "approved",
    )
    create_reservation(
        users["boss"],
        clubs["airon"],
        rooms["K320"],
        "Laboratorium projektowe",
        "Praca projektowa w małych zespołach.",
        now + timedelta(days=8, hours=1),
        now + timedelta(days=8, hours=3),
        24,
        "pending",
    )
    create_reservation(
        users["boss"],
        clubs["airon"],
        rooms["A01"],
        "Odrzucony test terminu",
        "Rezerwacja pokazowa odrzucona z uzasadnieniem administracji.",
        now + timedelta(days=6, hours=1),
        now + timedelta(days=6, hours=2),
        30,
        "rejected",
        "Przykładowy powód odrzucenia w danych demonstracyjnych.",
    )
    for user in users.values():
        if not user.notifications:
            db.session.add(
                Notification(
                    user=user,
                    message_pl="Witaj w wersji demonstracyjnej StudentSpot.",
                    message_en="Welcome to the StudentSpot demo.",
                )
            )

    db.session.commit()


def feature(code: str, name_pl: str, name_en: str, category: str = "equipment") -> RoomFeature:
    return get_or_create(
        RoomFeature,
        code=code,
        defaults={"name_pl": name_pl, "name_en": name_en, "category": category},
    )


def seed_majors(source_date: date) -> dict[str, Major]:
    majors: dict[str, Major] = {}
    for slug, name_pl, name_en, source_url in MAJOR_SOURCE_DATA:
        item = Major.query.filter((Major.slug == slug) | (Major.name_pl == name_pl)).first()
        if item is None:
            item = Major(slug=slug, name_pl=name_pl, name_en=name_en)
            db.session.add(item)
            db.session.flush()
        item.slug = slug
        item.name_en = name_en
        item.source_url = source_url
        item.verification_status = "official_source"
        item.last_verified_at = source_date
        if not item.dean_contact_pl:
            item.dean_contact_pl = "Kontakt do dziekana dostępny w oficjalnym serwisie AHE."
        if not item.dean_contact_en:
            item.dean_contact_en = "Dean contact is available on the official AHE website."
        majors[slug] = item
    return majors


def seed_clubs(guardian: User, majors: dict[str, Major], source_date: date) -> dict[str, Club]:
    clubs: dict[str, Club] = {}
    for data in CLUB_SOURCE_DATA:
        linked_majors = [majors[slug] for slug in data["major_slugs"]]
        item = club(
            slug=data["slug"],
            name_pl=data["name_pl"],
            name_en=data["name_en"],
            description_pl=data["description_pl"],
            description_en=data["description_en"],
            contact_email=data["contact_email"],
            guardian=guardian,
            majors=linked_majors,
            source_url=data["source_url"],
            website_url=data["website_url"],
            guardian_name=data["guardian_name"],
            tags=data["tags"],
            suggested_rooms=data["suggested_rooms"],
            verification_status=data["verification_status"],
            is_public=data["is_public"],
            is_featured=data["is_featured"],
            last_verified_at=source_date,
        )
        clubs[data["slug"]] = item
    return clubs


def club(
    slug: str,
    name_pl: str,
    name_en: str,
    description_pl: str,
    description_en: str,
    contact_email: str | None,
    guardian: User,
    majors: list[Major],
    source_url: str | None,
    website_url: str | None,
    guardian_name: str | None,
    tags: list[str],
    suggested_rooms: list[str],
    verification_status: str,
    is_public: bool,
    is_featured: bool,
    last_verified_at: date,
) -> Club:
    org = get_or_create(
        Organization,
        name_pl=name_pl,
        defaults={"name_en": name_en, "kind": "club", "description_pl": description_pl, "description_en": description_en},
    )
    org.name_en = name_en
    org.description_pl = description_pl
    org.description_en = description_en
    item = Club.query.filter((Club.slug == slug) | (Club.name_pl == name_pl)).first()
    if item is None:
        item = Club(
            organization=org,
            guardian=guardian,
            slug=slug,
            name_pl=name_pl,
            name_en=name_en,
            description_pl=description_pl,
            description_en=description_en,
        )
        db.session.add(item)
    item.organization = org
    item.guardian = guardian
    item.slug = slug
    item.name_pl = name_pl
    item.name_en = name_en
    item.description_pl = description_pl
    item.description_en = description_en
    item.campus = "lodz"
    item.guardian_name = guardian_name
    item.contact_email = contact_email
    item.source_url = source_url
    item.website_url = website_url
    item.tags_csv = ", ".join(tags)
    item.suggested_rooms_csv = ", ".join(suggested_rooms)
    item.verification_status = verification_status
    item.is_public = is_public
    item.is_featured = is_featured
    item.last_verified_at = last_verified_at
    item.majors = majors
    return item


def membership(user: User, club: Club, status: str, role: str) -> ClubMembership:
    existing = ClubMembership.query.filter_by(user_id=user.id, club_id=club.id).first()
    if existing:
        return existing
    item = ClubMembership(user=user, club=club, status=status, club_role=role)
    db.session.add(item)
    db.session.flush()
    return item


def room(
    code: str,
    name: str,
    building: str,
    address: str,
    capacity: int,
    room_type: str,
    description_pl: str,
    description_en: str,
    features: list[RoomFeature],
    source_url: str | None,
    verification_status: str,
    floor: str | None = None,
    photo_url: str | None = None,
) -> Room:
    existing = Room.query.filter_by(code=code).first()
    if existing:
        return existing
    item = Room(
        code=code,
        name=name,
        building=building,
        floor=floor,
        address=address,
        capacity=capacity,
        room_type=room_type,
        description_pl=description_pl,
        description_en=description_en,
        location_hint_pl="Sprawdź mapę budynku przed wydarzeniem.",
        location_hint_en="Check the building map before the event.",
        map_url="media/rooms/sterlinga-plan.webp",
        photo_url=photo_url,
        source_type="source" if verification_status == "verified" else "user_provided",
        source_url=source_url,
        verification_status=verification_status,
        last_verified_at=date(2026, 6, 14) if verification_status == "verified" else None,
    )
    item.features = features
    db.session.add(item)
    db.session.flush()
    return item


def create_reservation(
    user: User,
    club: Club,
    room: Room,
    title: str,
    description: str,
    starts_at: datetime,
    ends_at: datetime,
    participants: int,
    status: str,
    reason: str | None = None,
) -> Reservation:
    existing = Reservation.query.filter_by(title=title, room_id=room.id).first()
    if existing:
        return existing
    item = Reservation(
        created_by=user,
        club=club,
        room=room,
        title=title,
        description=description,
        starts_at=starts_at,
        ends_at=ends_at,
        participants=participants,
        status=status,
        rejection_reason=reason,
        requires_step_free_access=True,
        requires_elevator=True,
    )
    db.session.add(item)
    db.session.flush()
    db.session.add(
        ReservationStatusHistory(
            reservation=item,
            from_status=None,
            to_status=status,
            note=reason or "seed",
            changed_by=user,
        )
    )
    if status == "approved":
        db.session.add(
            Event(
                reservation=item,
                club=club,
                room=room,
                title=title,
                description=description,
                starts_at=starts_at,
                ends_at=ends_at,
                visibility="members",
                planned_participants=participants,
                accessibility_summary="Dostęp windą i bezstopniowe wejście.",
            )
        )
    return item
