# Prompt do Codex — StudentSpot

Skopiuj cały prompt do Codex w katalogu repozytorium. Do repozytorium dodaj wcześniej:

- `00_README_STUDENTSPOT.md`
- `01_STUDENTSPOT_SPECYFIKACJA_MVP.md`
- `02_STUDENTSPOT_DANE_I_ZRODLA.md`

---

## PROMPT

Pracujesz w repozytorium projektu **StudentSpot**. Masz zbudować kompletne MVP aplikacji, nie tylko plan lub makietę.

Przed pierwszą zmianą:

1. przeczytaj wszystkie pliki `*_STUDENTSPOT_*.md`,
2. sprawdź aktualną zawartość repozytorium,
3. zachowaj każdą istniejącą działającą funkcję,
4. utwórz plan implementacji w `IMPLEMENTATION_PLAN.md`,
5. rozpocznij pracę od najmniejszej kompletnej ścieżki użytkownika.

### Definicja sukcesu

Projekt jest zakończony, gdy użytkownik może:

1. zarejestrować konto studenta,
2. aktywować konto,
3. zalogować się,
4. złożyć wniosek o członkostwo w kole,
5. otrzymać zatwierdzoną rolę przewodniczącego,
6. wyszukać salę według daty, liczby osób, wyposażenia i dostępności,
7. złożyć rezerwację,
8. otrzymać decyzję administratora,
9. zobaczyć wydarzenie na dashboardzie,
10. przełączyć interfejs PL / EN.

### Stack

- Python + Flask,
- Jinja2,
- SQLAlchemy,
- PyMySQL dla produkcji,
- SQLite dla lokalnego testu,
- Flask-WTF,
- Gunicorn,
- minimalny CSS i JavaScript,
- pytest.

Nie używaj:

- React,
- Next.js,
- Vue,
- osobnego Node backendu,
- Docker jako wymogu wdrożenia,
- Redis,
- Celery,
- Keycloak,
- lokalnego MySQL na Frog,
- ciężkich frameworków administracyjnych.

### Wymagania implementacyjne

#### Repozytorium

- uporządkowana architektura Flask application factory,
- blueprints,
- typowanie tam, gdzie zwiększa czytelność,
- czytelne nazwy po angielsku w kodzie,
- interfejs po polsku i angielsku,
- lint i testy.

#### Bezpieczeństwo

- hasła hashowane,
- tokeny aktywacyjne hashowane,
- CSRF,
- autoryzacja na poziomie tras i usług,
- limit logowania,
- bezpieczne cookie,
- walidacja serwerowa,
- brak PII w logach,
- brak danych medycznych,
- `.env` poza repozytorium.

#### Role

Globalne:

- student,
- club_guardian,
- property_admin,
- system_admin,
- utw_organizer.

W kole:

- chair,
- vice_chair,
- secretary,
- treasurer,
- member.

Rezerwować mogą tylko chair, vice_chair, club_guardian, utw_organizer i administratorzy.

#### Konflikt rezerwacji

Zaimplementuj poprawny warunek nakładania przedziałów:

```text
new_start < existing_end AND new_end > existing_start
```

Konflikt dotyczy rezerwacji `pending` i `approved`, z wyjątkiem edytowanej rezerwacji.

#### Prywatność i dostępność

Nie dodawaj pola `is_disabled` do użytkownika.

Zamiast tego rezerwacja przechowuje cechy organizacyjne, np.:

- requires_step_free_access,
- requires_elevator,
- requires_induction_loop,
- requires_accessible_computer,
- accessibility_notes — bez diagnozy i szczegółów zdrowotnych.

#### E-mail

Zaimplementuj abstrakcję `EmailService`:

- `SmtpEmailService`,
- `ConsoleEmailService` dla developmentu.

Produkcja ma korzystać z SMTP przez zmienne środowiskowe. Nie koduj danych Gmaila w repozytorium.

#### Design

- jasny, minimalistyczny interfejs,
- branding inspirowany AHE,
- oficjalne logotypy tylko z oficjalnego źródła,
- fallback tekstowy,
- stopka o nieoficjalnym charakterze projektu,
- mobile-first,
- WCAG-oriented.

### Kolejność commitów / etapów

1. `chore: initialize flask app and configuration`
2. `feat: add users authentication and email verification`
3. `feat: add majors clubs and membership workflow`
4. `feat: add rooms features and availability search`
5. `feat: add reservation approval workflow`
6. `feat: add events dashboard and notifications`
7. `feat: add bilingual interface and accessibility`
8. `test: cover critical business flows`
9. `docs: add frog deployment and project documentation`

Jeżeli środowisko nie pozwala tworzyć commitów, zachowaj ten podział w raporcie zmian.

### Testy minimalne

- unikalność indeksu,
- unikalność e-maila,
- aktywacja tokenem,
- token wygasły,
- blokada nieaktywnego konta,
- membership pending / approved / rejected,
- kontrola roli,
- wyszukiwanie po pojemności,
- wyszukiwanie po cechach,
- konflikt czasu,
- brak konfliktu na granicy przedziałów,
- approval,
- rejection reason,
- audit log,
- przełączenie języka,
- 403 dla nieuprawnionych.

### Dane startowe

Użyj `02_STUDENTSPOT_DANE_I_ZRODLA.md`.

Dla każdego rekordu dodaj:

- source_url,
- verification_status,
- last_verified_at.

Dane K320 i K200A oznacz jako `unverified`.

Dodaj AIrON wraz z oficjalnymi linkami AHE. Nie kopiuj nazwisk studentów do kont demo.

### Dokumentacja pod zaliczenie

W `docs/PROJECT_REPORT.md` opisz dokładnie:

1. miejsce użytkowania i schemat organizacyjny,
2. problem, cel, zakres, procesy i dokumenty wynikowe,
3. użytkowników, role i uprawnienia,
4. założenia i systemy zewnętrzne,
5. wymagania funkcjonalne,
6. wymagania niefunkcjonalne,
7. projekt koncepcyjny i przepływy informacji.

Dodaj:

- Mermaid ERD,
- Mermaid flowchart,
- tabelę traceability: wymaganie → moduł → test,
- scenariusz demonstracji.

### Deployment na Frog

Przygotuj instrukcję dla Alpine Linux:

- pakiety systemowe,
- venv,
- instalacja requirements,
- odczyt danych MySQL z `/root/mysql.txt`,
- migracja / inicjalizacja bazy,
- seed,
- uruchomienie Gunicorn na `${APP_PORT}`,
- subdomena `frogXX-PORT.wykr.es`,
- health check,
- restart i logi.

Użyj:

```bash
gunicorn --workers 1 --threads 2 --timeout 60 --bind 0.0.0.0:${APP_PORT} wsgi:app
```

Nie konfiguruj HTTPS wewnątrz aplikacji dla `wykr.es`; aplikacja ma nasłuchiwać po HTTP na porcie Froga.

### Sposób pracy

- działaj autonomicznie,
- nie zatrzymuj się po wygenerowaniu szkieletu,
- uruchamiaj testy po każdej fazie,
- naprawiaj błędy,
- wykonaj finalne `pytest`,
- wykonaj kontrolę importów i start aplikacji,
- na końcu podaj listę utworzonych plików, testów i instrukcję uruchomienia.

Zacznij od audytu repozytorium i planu, a następnie od razu przejdź do implementacji.
