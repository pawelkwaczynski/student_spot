# StudentSpot - plan realizacji do oddania

## Cel

Zbudowac kompletne MVP aplikacji StudentSpot jako lekka aplikacja Flask/Jinja2 gotowa do lokalnego uruchomienia, spakowania do `.zip` oraz wdrozenia na Mikrus Frog.

## Zakres obowiazkowy

1. Rejestracja studenta z walidacja numeru indeksu, e-maila, nicku i hasla.
2. Aktywacja konta kodem e-mail lub kodem z konsoli developerskiej.
3. Logowanie, wylogowanie, dashboard i podstawowa edycja profilu.
4. Katalog kierunkow, kol naukowych i wydarzen.
5. Wniosek o czlonkostwo oraz decyzja opiekuna/admina.
6. Role globalne i role w kole, w tym uprawnienie do rezerwacji tylko dla wybranych rol.
7. Katalog sal z filtrowaniem po dacie, godzinach, pojemnosci, wyposazeniu i wymaganiach dostepnosciowych.
8. Rezerwacje sal z warunkiem konfliktu `new_start < existing_end AND new_end > existing_start`.
9. Panel administracyjny do zatwierdzania/odrzucania czlonkostw i rezerwacji.
10. Historia statusow, powiadomienia w aplikacji, zdarzenia i podstawowy audyt.
11. Interfejs PL/EN, dark mode, wysoki kontrast i wieksza czcionka.
12. Dostepnosc: semantyczny HTML, widoczny focus, etykiety formularzy, komunikaty bledow, brak znaczenia tylko kolorem.
13. Seed demonstracyjny zgodny z materialami w `source_info/`.
14. Testy krytycznych procesow.
15. Dokumentacja projektu, wdrozenia Frog i instrukcja demo.

## Stack

- Python + Flask
- Jinja2
- SQLAlchemy
- Flask-WTF / CSRF
- SQLite lokalnie
- PyMySQL dla Frog/MySQL
- Gunicorn
- pytest
- HTML/CSS/minimalny JavaScript bez SPA

## Etapy pracy

### 1. Porzadkowanie repozytorium

- Utworzyc `source_info/`.
- Przeniesc materialy z katalogu startowego do `source_info/`.
- Zostawic w katalogu glownym tylko kod, dokumentacje wynikowa, konfiguracje, testy i paczke ZIP.
- Skopiowac logotypy z `source_info/` do `app/static/media/brand/`.

### 2. Szkielet aplikacji

- `app/__init__.py` z application factory.
- `app/config.py`, `app/extensions.py`.
- Blueprinty: `main`, `auth`, `clubs`, `rooms`, `reservations`, `admin`.
- `wsgi.py`, `manage.py`, `requirements.txt`, `.env.example`.
- `/health`.

### 3. Dane i modele

- Modele: users, tokens, majors, organizations, clubs, memberships, rooms, room_features, room_unavailability, reservations, reservation_status_history, events, notifications, audit_logs.
- Indeksy, unikalnosci i relacje.
- Helpery serwisowe do konfliktow, uprawnien, audytu i powiadomien.

### 4. Workflow rejestracji i czlonkostwa

- Formularze Flask-WTF.
- Hashowanie hasel i tokenow aktywacyjnych.
- ConsoleEmailService dla developmentu i SmtpEmailService dla produkcji.
- Wnioski czlonkowskie i decyzje admin/opiekun.
- Nadanie roli przewodniczacego w danych demo.

### 5. Sale, rezerwacje i wydarzenia

- Katalog sal i filtry.
- Ranking dopasowania.
- Tworzenie rezerwacji przez uprawnione role.
- Zatwierdzenie tworzy wydarzenie.
- Odrzucenie wymaga powodu.
- Historia statusow i powiadomienia.

### 6. UI, PL/EN i dostepnosc

- Slowniki tlumaczen `app/translations/pl.py` i `app/translations/en.py`.
- Przelacznik PL/EN.
- Dark mode, high contrast i wieksza czcionka zapisywane w localStorage/cookie.
- CSS tokenowy: kolory jasne/ciemne, akcent czerwony, granat/grafit.
- Responsywny layout i widoczny focus.

### 7. Testy

Minimalne testy:

- duplikat indeksu i e-maila,
- aktywacja poprawna i wygasla,
- blokada nieaktywnego konta,
- membership pending/approved/rejected,
- 403 dla nieuprawnionych,
- filtrowanie sal po pojemnosci i cechach,
- konflikt i brak konfliktu na granicy przedzialow,
- approval/rejection reason,
- audit log,
- przelaczenie jezyka.

### 8. Dokumentacja i Frog

- `README.md` po polsku.
- `docs/PROJECT_REPORT.md` z ERD, flowchartem i traceability.
- `docs/FROG_DEPLOYMENT.md`.
- `deploy_frog.sh`.
- `scripts/package_release.sh` tworzacy ZIP bez venv/cache.

### 9. Finalizacja

- `pytest`.
- Smoke test importu i startu aplikacji.
- Security review: sekrety, PII w logach, autoryzacja, CSRF, SQL injection, cookie.
- Utworzenie `student_spot.zip`.
- Aktualizacja `PROGRESS.md`.

## Ograniczenia i decyzje

- Projekt jest nieoficjalnym prototypem studenckim, co musi byc widoczne w stopce i dokumentacji.
- Zakres sal zostal ograniczony przez uzytkownika do budynku przy Sterlinga 26. Nie dodawac G1/G2 ani sal z Rewolucji 1905 r.
- Konta demonstracyjne maja byc proste i fejkowe: admin, property admin, opiekun, `boss` jako przewodniczacy/kierownik kola, vice, zwykly czlonek, pending student i UTW organizer.
- Nie zapisujemy diagnoz medycznych ani pola `is_disabled` na uzytkowniku.
- Nie uzywamy React/Next/Docker/Redis/Celery/Keycloak.
- Wdrozenie produkcyjne na Frog wymaga danych konta, portu i dostepu SSH; bez nich przygotowujemy paczke i instrukcje, a samo wyslanie wykonujemy dopiero gdy srodowisko jest dostepne.
