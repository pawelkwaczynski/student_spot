from datetime import datetime, timedelta

from app.extensions import db
from app.models import (
    AuditLog,
    Club,
    ClubMembership,
    ClubMessage,
    ClubMessageRecipient,
    EmailVerificationToken,
    Notification,
    Reservation,
    Room,
    User,
)
from app.services import has_room_conflict, search_rooms
from tests.conftest import login


def test_demo_seed_uses_eight_accounts_and_sterlinga_only(app):
    with app.app_context():
        emails = {user.email for user in User.query.order_by(User.email).all()}
        demo_emails = {
            "admin@studentspot.example.com",
            "boss@studentspot.example.com",
            "guardian@studentspot.example.com",
            "member@studentspot.example.com",
            "pending@studentspot.example.com",
            "property@studentspot.example.com",
            "utw@studentspot.example.com",
            "vice@studentspot.example.com",
        }
        assert demo_emails.issubset(emails)
        assert User.query.filter(User.email.in_(demo_emails)).count() == 8
        assert "ada.airon@studentspot.example.com" in emails
        assert "jan.pending@studentspot.example.com" in emails
        assert {room.address for room in Room.query.all()} == {"Sterlinga 26"}
        assert Room.query.filter(Room.code.in_(("G1", "G2"))).count() == 0
        assert Room.query.filter_by(code="K320").one().floor == "II"
        assert Room.query.filter_by(code="K200A").one().floor == "II"


def test_scientific_club_seed_public_visibility_and_hidden_records(client, app):
    with app.app_context():
        assert Club.query.count() == 13
        assert Club.query.filter_by(is_public=True).count() == 7
        assert Club.query.filter_by(is_public=False).count() == 6
        assert Club.query.filter_by(slug="airon").one().guardian_name == "mgr inż. Zoltan Farkas"
    response = client.get("/clubs")
    assert response.status_code == 200
    assert "Koło Naukowe AIrON".encode() in response.data
    assert "Moja Psychologia".encode() not in response.data


def test_club_filters_and_dashboard_recommendations(client):
    response = client.get("/clubs?major=informatyka&q=AI")
    assert response.status_code == 200
    assert "Koło Naukowe AIrON".encode() in response.data
    assert "Koło Naukowe Progressus".encode() not in response.data
    login(client, "boss@studentspot.example.com")
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"My account" in response.data
    assert b"AIrON" in response.data
    assert "Błażej Strus".encode() in response.data
    assert b"Sala K320" in response.data
    assert b"AIrON development roadmap" in response.data


def test_language_switch_changes_interface(client):
    response = client.get("/set-language/en", follow_redirects=True)
    assert response.status_code == 200
    assert b'Manage club activity and room bookings without chaos.' in response.data


def test_home_page_contains_news_feed_below_clubs(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Koła".encode() in response.data
    assert response.data.count(b"club-logo-frame") == 7
    assert "Aktualności".encode() in response.data
    assert "Roadmapa rozwoju Koła Naukowego AIRON".encode() in response.data
    assert "Templatki aktualności kół naukowych na podstawie prawdziwych materiałów.".encode() in response.data


def test_media_page_contains_press_note_and_downloads(client):
    response = client.get("/media")
    assert response.status_code == 200
    assert "Notatka prasowa".encode() in response.data
    assert b"studentspot-logo.png" in response.data
    assert b"studentspot-popup-welcome.png" in response.data
    assert b"studentspot-ahe-ambassadors-overview.png" not in response.data
    assert b"studentspot-ahe-ambassadors-experts.png" not in response.data
    assert "O autorze".encode() not in response.data
    assert "Key visual AHE".encode() not in response.data
    assert response.data.count(b"download=") == 6


def test_info_page_contains_author_kv_and_project_map(client):
    response = client.get("/info")
    assert response.status_code == 200
    assert "Kontekst projektu".encode() in response.data
    assert "Paweł Kwaczyński".encode() in response.data
    assert b"165318" in response.data
    assert b"kwaczynski.pawel@gmail.com" in response.data
    assert "Członek Studenckiego Koła Naukowego AIRON".encode() in response.data
    assert b"view-source:https://www.ahe.lodz.pl//themes/custom/ahe/css/style.css" in response.data
    assert b"source_info/studentspot_people_package" not in response.data
    assert "Mapa wymagań projektowych".encode() in response.data
    assert "Schemat organizacyjny AHE".encode() in response.data
    assert "Wymagania funkcjonalne".encode() in response.data
    assert "Wymagania niefunkcjonalne".encode() in response.data
    assert "Projekt koncepcyjny i przepływy informacyjne".encode() in response.data
    assert "Katalog 7 publicznie pokazanych kół AHE".encode() in response.data
    assert "repozytorium lokalne i GitHub".encode() in response.data
    assert "Metodyka zarządzania informacją.</p>".encode() in response.data
    assert "UTW AHE = Uniwersytet Trzeciego Wieku".encode() in response.data
    assert "Model kont UTW i komunikatów".encode() in response.data


def test_info_page_professor_map_is_translated_to_english(client):
    client.get("/set-language/en")
    response = client.get("/info")
    assert response.status_code == 200
    assert b"Project requirements map" in response.data
    assert b"Usage place and organization" in response.data
    assert b"Functional requirements" in response.data
    assert b"Non-functional requirements" in response.data
    assert b"Conceptual design and information flows" in response.data


def test_demo_page_mentions_accounts_and_author_context_without_kv(client):
    response = client.get("/demo")
    assert response.status_code == 200
    assert "Konta demo".encode() in response.data
    assert "Key visual AHE".encode() not in response.data
    assert b"keyvisual_info.md" not in response.data
    assert "Model kont UTW i komunikatów".encode() not in response.data
    assert "Paweł Kwaczyński".encode() in response.data
    assert b"165318" in response.data
    assert "Szybki tutorial pokazowy".encode() in response.data
    assert "Sugerowane workflow: demo MVP pozwala odtworzyć pełny przepływ".encode() in response.data
    assert "Zachęcam do testowania!".encode() in response.data
    assert "członkowie koła, statusy, role, wiadomości".encode() in response.data


def test_news_calendar_and_local_heroes_pages(client):
    response = client.get("/news")
    assert response.status_code == 200
    assert "Roadmapa rozwoju Koła Naukowego AIRON".encode() in response.data
    assert "opiekunowie i osoby odpowiedzialne za komunikację koła".encode() in response.data
    assert "bossowie".encode() not in response.data
    assert b"roadmap.png" in response.data
    response = client.get("/calendar")
    assert response.status_code == 200
    assert b"2026-06-16" in response.data
    assert "Sala K320".encode() in response.data
    response = client.get("/local-heroes")
    assert response.status_code == 200
    assert "Adrian Makoć".encode() in response.data
    assert "FACT-CHECKING I PRZECIWDZIAŁANIE DEZINFORMACJI".encode() in response.data
    assert b"adrian-makoc.webp" in response.data
    assert "Osobna przestrzeń dla lokalnych liderów, ambasadorów i ekspertów AHE.<br>".encode() in response.data
    assert response.data.count(b'class="local-hero-feature"') == 23
    assert b"ambassador-icon.png" not in response.data


def test_duplicate_index_and_email_are_rejected(client):
    response = client.post(
        "/auth/register",
        data={
            "index_number": "165320",
            "first_name": "Ada",
            "last_name": "Test",
            "nickname": "newnick",
            "email": "member@studentspot.example.com",
            "password": "VeryStrong123!",
            "confirm_password": "VeryStrong123!",
            "major_id": "1",
            "year_of_study": "1",
            "study_level": "first_cycle",
            "study_mode": "part_time",
            "accept_terms": "y",
            "accept_privacy": "y",
        },
    )
    assert response.status_code == 200
    assert b"Index already exists" in response.data
    assert b"E-mail already exists" in response.data


def test_registration_activation_flow(client, app):
    response = client.post(
        "/auth/register",
        data={
            "index_number": "165399",
            "first_name": "New",
            "last_name": "Student",
            "nickname": "new-student",
            "email": "new@studentspot.example.com",
            "password": "VeryStrong123!",
            "confirm_password": "VeryStrong123!",
            "major_id": "1",
            "year_of_study": "1",
            "study_level": "first_cycle",
            "study_mode": "part_time",
            "accept_terms": "y",
            "accept_privacy": "y",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with client.session_transaction() as sess:
        code = sess["dev_activation_code"]
    response = client.post("/auth/activate", data={"code": code}, follow_redirects=True)
    assert response.status_code == 200
    assert "Znajdź swoje koło naukowe".encode() in response.data
    with app.app_context():
        user = User.query.filter_by(email="new@studentspot.example.com").one()
        assert user.is_active
        assert user.study_level == "first_cycle"
        assert user.study_mode == "part_time"
        assert user.email_verified_at is not None
        assert user.terms_accepted_at is not None
        assert user.privacy_accepted_at is not None
        assert EmailVerificationToken.query.filter_by(user_id=user.id).one().used_at is not None


def test_registration_allows_blank_nickname(client, app):
    response = client.post(
        "/auth/register",
        data={
            "index_number": "165398",
            "first_name": "No",
            "last_name": "Nickname",
            "nickname": "",
            "email": "blank-nickname@studentspot.example.com",
            "password": "VeryStrong123!",
            "confirm_password": "VeryStrong123!",
            "major_id": "1",
            "year_of_study": "1",
            "study_level": "first_cycle",
            "study_mode": "part_time",
            "accept_terms": "y",
            "accept_privacy": "y",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email="blank-nickname@studentspot.example.com").one()
        assert user.nickname == "student-165398"


def test_activation_code_is_hidden_when_dev_display_disabled(client, app):
    app.config["SHOW_DEV_ACTIVATION_CODE"] = False
    response = client.post(
        "/auth/register",
        data={
            "index_number": "165397",
            "first_name": "Hidden",
            "last_name": "Code",
            "nickname": "hidden-code",
            "email": "hidden-code@studentspot.example.com",
            "password": "VeryStrong123!",
            "confirm_password": "VeryStrong123!",
            "major_id": "1",
            "year_of_study": "1",
            "study_level": "first_cycle",
            "study_mode": "part_time",
            "accept_terms": "y",
            "accept_privacy": "y",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Test code:" not in response.data
    with client.session_transaction() as sess:
        assert "dev_activation_code" not in sess
    with app.app_context():
        user = User.query.filter_by(email="hidden-code@studentspot.example.com").one()
        assert EmailVerificationToken.query.filter_by(user_id=user.id).count() == 1


def test_student_without_approved_role_cannot_reserve(client):
    login(client, "member@studentspot.example.com")
    response = client.get("/reservations/new")
    assert response.status_code == 403


def test_boss_can_open_reservation_form(client):
    login(client, "boss@studentspot.example.com")
    response = client.get("/reservations/new")
    assert response.status_code == 200
    assert b"Create reservation" in response.data or b"Utw" in response.data
    assert b"Reservations only for authorized users" in response.data
    assert b"approved club representative" in response.data
    assert b"Arrange free transport from the Lodz area" in response.data
    assert b"from any place in Lodz" not in response.data


def test_accessibility_support_requests_are_saved_in_reservation_notes(client, app):
    login(client, "vice@studentspot.example.com")
    response = client.post(
        "/reservations/new",
        data={
            "club_id": "1",
            "room_id": "1",
            "title": "Test dostępności",
            "description": "Spotkanie testowe z potrzebami organizacyjnymi dostępności.",
            "event_type": "meeting",
            "date": "2026-12-20",
            "start_time": "10:00",
            "end_time": "11:00",
            "participants": "12",
            "requires_sign_language_interpreter": "y",
            "requires_blind_guide": "y",
            "requires_accessible_transport": "y",
            "requires_assistive_equipment": "y",
            "accessibility_notes": "Prośba o kontakt z uczestnikiem dzień wcześniej.",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        reservation = Reservation.query.filter_by(title="Test dostępności").one()
        assert "Potrzeby organizacyjne dostępności" in reservation.accessibility_notes
        assert "tłumacza języka migowego" in reservation.accessibility_notes
        assert "przewodnika dla osoby niewidomej" in reservation.accessibility_notes
        assert "bezpłatnego transportu z terenu Łodzi" in reservation.accessibility_notes
        assert "sprzętu wspomagającego" in reservation.accessibility_notes


def test_approved_meeting_can_be_downloaded_as_ics(client, app):
    login(client, "vice@studentspot.example.com")
    with app.app_context():
        reservation_id = Reservation.query.filter_by(title="Warsztat AIrON").one().id
    response = client.get(f"/reservations/{reservation_id}/calendar.ics")
    assert response.status_code == 200
    assert response.mimetype == "text/calendar"
    assert b"BEGIN:VCALENDAR" in response.data
    assert b"SUMMARY:Warsztat AIrON" in response.data


def test_room_search_by_capacity_and_features(app):
    with app.app_context():
        matches = search_rooms(participants=80, feature_codes=["projector"])
        codes = [room.code for room in matches]
        assert "A02" in codes
        assert "A04" in codes
        assert "K320" not in codes
        computer_matches = search_rooms(participants=30, feature_codes=["computers"])
        assert {room.code for room in computer_matches} == {"K320", "K200A"}
        best_fit = search_rooms(participants=23)
        assert best_fit[0].code == "S01"


def test_room_filters_empty_state_mentions_modernization(client):
    response = client.get("/rooms?features=microphone&accessibility=induction_loop")
    assert response.status_code == 200
    assert "Brak sal dla wybranych filtrów".encode() in response.data
    assert "modernizowana".encode() in response.data


def test_reservation_conflict_and_boundary_rule(app):
    with app.app_context():
        reservation = Reservation.query.filter_by(title="Warsztat AIrON").one()
        assert has_room_conflict(
            reservation.room_id,
            reservation.starts_at + timedelta(minutes=30),
            reservation.ends_at + timedelta(minutes=30),
        )
        assert not has_room_conflict(
            reservation.room_id,
            reservation.ends_at,
            reservation.ends_at + timedelta(hours=1),
        )


def test_admin_rejection_requires_reason(client, app):
    login(client, "admin@studentspot.example.com")
    with app.app_context():
        reservation = Reservation.query.filter_by(status="pending").first()
        reservation_id = reservation.id
    response = client.post(
        f"/admin/reservations/{reservation_id}/decision",
        data={"action": "reject", "rejection_reason": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Reservation, reservation_id).status == "pending"


def test_admin_can_approve_membership_and_audit_is_recorded(client, app):
    login(client, "admin@studentspot.example.com")
    with app.app_context():
        membership = (
            ClubMembership.query.join(ClubMembership.user)
            .filter(ClubMembership.status == "pending", User.email == "pending@studentspot.example.com")
            .one()
        )
        membership_id = membership.id
    response = client.post(
        f"/admin/memberships/{membership_id}/decision",
        data={"action": "approve", "club_role": "member"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(ClubMembership, membership_id).status == "approved"
        assert AuditLog.query.filter_by(action="membership_status_changed").count() >= 1


def test_guardian_sees_member_directory_and_can_update_membership(client, app):
    login(client, "guardian@studentspot.example.com")
    response = client.get("/admin/")
    assert response.status_code == 200
    assert "Członkowie koła".encode() in response.data
    assert b"boss@studentspot.example.com" in response.data
    with app.app_context():
        membership = (
            ClubMembership.query.join(ClubMembership.user)
            .filter(User.email == "pending@studentspot.example.com")
            .one()
        )
        membership_id = membership.id
    response = client.post(
        f"/admin/memberships/{membership_id}/decision",
        data={"action": "approve", "club_role": "secretary"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        membership = db.session.get(ClubMembership, membership_id)
        assert membership.status == "approved"
        assert membership.club_role == "secretary"


def test_property_admin_sees_room_decisions_not_member_management(client):
    login(client, "property@studentspot.example.com")
    response = client.get("/admin/")
    assert response.status_code == 200
    assert "Wnioski rezerwacyjne".encode() in response.data
    assert "Komunikat do UTW".encode() in response.data
    assert "Członkowie koła".encode() not in response.data
    assert "Wnioski członkowskie".encode() not in response.data


def test_guardian_can_send_message_to_club_members_and_member_reads_it(client, app):
    login(client, "guardian@studentspot.example.com")
    with app.app_context():
        club = Club.query.filter_by(slug="airon").one()
        club_id = club.id
    response = client.post(
        "/messages/compose",
        data={
            "club_id": str(club_id),
            "subject": "Plan spotkania koła",
            "body": "Przynieście krótką listę tematów na kolejne warsztaty.",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Wiadomość została wysłana do członków koła.".encode() in response.data
    with app.app_context():
        message = ClubMessage.query.filter_by(subject="Plan spotkania koła").one()
        assert len(message.recipients) >= 4
        boss = User.query.filter_by(email="boss@studentspot.example.com").one()
        boss_item = ClubMessageRecipient.query.filter_by(message_id=message.id, recipient_id=boss.id).one()
        assert boss_item.read_at is None
        assert Notification.query.filter(
            Notification.user_id == boss.id,
            Notification.message_pl.contains("Plan spotkania koła"),
        ).count() == 1
        boss_item_id = boss_item.id
    login(client, "boss@studentspot.example.com")
    response = client.get("/messages/")
    assert response.status_code == 200
    assert b"Plan spotkania ko" in response.data
    response = client.get(f"/messages/{boss_item_id}")
    assert response.status_code == 200
    assert "Przynieście krótką listę tematów".encode() in response.data
    with app.app_context():
        assert db.session.get(ClubMessageRecipient, boss_item_id).read_at is not None


def test_admin_can_confirm_hidden_club_and_send_utw_announcement(client, app):
    login(client, "admin@studentspot.example.com")
    with app.app_context():
        club = Club.query.filter_by(slug="moja-psychologia").one()
        club_id = club.id
        assert not club.is_public
    response = client.post(f"/admin/clubs/{club_id}/confirm", follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        club = db.session.get(Club, club_id)
        assert club.is_public
        assert club.verification_status == "active_verified"
    response = client.post("/admin/utw-announcements", data={"message": "Spotkanie organizacyjne"}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        utw = User.query.filter_by(email="utw@studentspot.example.com").one()
        assert Notification.query.filter(
            Notification.user_id == utw.id,
            Notification.message_pl.contains("Spotkanie organizacyjne"),
        ).count() == 1
