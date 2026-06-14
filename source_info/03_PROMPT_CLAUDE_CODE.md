# Prompt do Claude Code — StudentSpot

Skopiuj cały tekst poniżej do Claude Code razem z plikami:

- `00_README_STUDENTSPOT.md`
- `01_STUDENTSPOT_SPECYFIKACJA_MVP.md`
- `02_STUDENTSPOT_DANE_I_ZRODLA.md`

---

## PROMPT

Jesteś głównym architektem, programistą full-stack, testerem i technical writerem projektu StudentSpot.

Twoim zadaniem jest zbudowanie kompletnego, lekkiego i działającego MVP zgodnie z trzema załączonymi plikami Markdown. Najpierw przeczytaj je w całości. Nie zaczynaj implementacji, dopóki nie przygotujesz krótkiej analizy wymagań i planu prac.

### Cel

Zbuduj aplikację webową StudentSpot na ocenę 5/5 z przedmiotu dotyczącego systemów informatycznych zarządzania. System ma obsługiwać koła naukowe, członkostwa, role, wydarzenia, katalog sal, filtrowanie dostępności, rezerwacje i workflow zatwierdzania.

### Twarde ograniczenia

1. Hosting docelowy: Mikrus Frog.
2. Ograniczenia środowiska: 256 MB RAM, 3 GB dysku, Alpine Linux.
3. Nie używaj React, Next.js, Node jako serwera, Dockera, Redis, Celery, lokalnego MySQL ani Keycloaka.
4. Użyj Python + Flask + Jinja2 + SQLAlchemy + MySQL / PyMySQL.
5. Frontend ma być serwerowo renderowany, responsywny i dostępny.
6. Gunicorn: maksymalnie 1 worker i 2 threads.
7. Aplikacja musi działać również lokalnie z SQLite.
8. Wszystkie sekrety w zmiennych środowiskowych.
9. Kod ma być prosty, dobrze skomentowany i zrozumiały dla studenta informatyki.

### Kolejność pracy

#### Etap 1 — analiza

- przeczytaj wszystkie pliki,
- wypisz wymagania funkcjonalne i niefunkcjonalne,
- wskaż ewentualne sprzeczności,
- nie pytaj o rzeczy, które można rozsądnie rozstrzygnąć na podstawie specyfikacji,
- przygotuj plan plików i modułów.

#### Etap 2 — szkielet

Utwórz strukturę podobną do:

```text
studentspot/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   ├── auth/
│   ├── clubs/
│   ├── rooms/
│   ├── reservations/
│   ├── admin/
│   ├── main/
│   ├── templates/
│   ├── static/
│   └── translations/
├── tests/
├── scripts/
├── migrations/
├── requirements.txt
├── .env.example
├── wsgi.py
├── seed.py
├── deploy_frog.sh
└── README.md
```

#### Etap 3 — model danych

Zaimplementuj modele ze specyfikacji. Wymagane:

- użytkownicy,
- tokeny aktywacyjne,
- kierunki,
- organizacje,
- koła,
- członkostwa,
- role w kole,
- sale,
- cechy sal,
- wyłączenia dostępności,
- rezerwacje,
- wymagane cechy,
- historia statusów,
- wydarzenia,
- powiadomienia,
- audyt.

Dodaj:

- constraints,
- indeksy,
- enumy,
- poprawne relacje,
- kaskady tylko tam, gdzie są bezpieczne.

#### Etap 4 — uwierzytelnianie

Zbuduj:

- rejestrację studenta,
- walidację indeksu, e-maila, nicku i hasła,
- aktywację kodem lub linkiem,
- login e-mail / indeks,
- bezpieczne hashowanie,
- reset hasła opcjonalnie,
- ograniczenie prób logowania,
- bezpieczne sesje,
- CSRF.

Nie zapisuj kodów aktywacyjnych jawnie.

#### Etap 5 — członkostwo

- rekomendacja kół według kierunku,
- wniosek „jestem członkiem” lub „chcę dołączyć”,
- akceptacja przez opiekuna / administratora,
- przypisanie roli,
- komunikat dla kierunku bez koła,
- link do dziekana konfigurowany w bazie.

#### Etap 6 — sale i rezerwacje

- katalog sal z kartami,
- zdjęcie, pojemność, wyposażenie, mapa, dostępność,
- filtry daty, czasu, pojemności i cech,
- algorytm rekomendacji,
- kontrola konfliktu,
- formularz rezerwacji,
- statusy i historia,
- zatwierdzanie przez administratora nieruchomości,
- wymagany powód odrzucenia.

Wymagania dostępnościowe mają opisywać wydarzenie. Nie zapisuj informacji o stanie zdrowia użytkownika.

#### Etap 7 — dashboard i wydarzenia

Dashboard ma zawierać:

- najbliższe spotkanie,
- liczbę nadchodzących wydarzeń,
- status członkostwa,
- status rezerwacji,
- CTA do rezerwacji dla uprawnionych.

Zatwierdzona rezerwacja może utworzyć wydarzenie.

#### Etap 8 — panel administracyjny

- kolejka rezerwacji,
- kalendarz,
- decyzja z komentarzem,
- zarządzanie salami i wyłączeniami,
- zarządzanie kołami i kierunkami,
- podstawowy audyt.

#### Etap 9 — PL / EN

- wszystkie elementy interfejsu mają wersję polską i angielską,
- użyj lekkich plików JSON lub słowników,
- nie instaluj ciężkiego systemu CMS,
- treści sal i kół mają pola PL / EN.

#### Etap 10 — design

Styl:

- minimalistyczny,
- zgodny wizualnie z AHE,
- dużo bieli,
- mocna hierarchia,
- czerwony akcent,
- grafitowy / granatowy tekst,
- estetyka premium, ale bez ciężkich animacji.

Pobierz oficjalne logotypy z linków w bazie wiedzy, jeżeli jest to technicznie możliwe. Nie hotlinkuj. Zapisz manifest źródeł. Jeżeli pobranie się nie powiedzie, zastosuj placeholder i jasno oznacz TODO.

Dodaj stopkę:

> Nieoficjalny projekt studencki — StudentSpot.

#### Etap 11 — dostępność

- semantyczny HTML,
- klawiatura,
- focus,
- etykiety,
- aria tylko gdy potrzebne,
- błędy formularzy dostępne dla czytników,
- kontrast,
- teksty alternatywne,
- test kluczowych ścieżek bez myszy.

#### Etap 12 — seed

Dodaj dane demonstracyjne zgodnie z bazą wiedzy. Dane niezweryfikowane oznacz jako niezweryfikowane. Nie twórz prawdziwych kont studentów z nazwiskami znalezionymi w internecie.

W seedzie koniecznie uwzględnij:

- AIrON,
- Koło Naukowe Grafiki,
- Warsztaty Emocji,
- Koło Kognitywistyki,
- Progressus,
- A01, A02, A03, A04, K320, K200A, G1, G2.

#### Etap 13 — testy

Napisz testy dla:

- rejestracji,
- duplikatu indeksu,
- aktywacji,
- uprawnień,
- wniosku członkowskiego,
- filtrowania sal,
- konfliktu rezerwacji,
- zatwierdzenia,
- obowiązkowego powodu odrzucenia,
- historii statusów,
- tłumaczeń,
- podstawowego audytu.

Uruchom testy i napraw wszystkie błędy.

#### Etap 14 — wdrożenie Frog

Przygotuj:

- `deploy_frog.sh`,
- `.env.example`,
- instrukcję konfiguracji współdzielonego MySQL z `/root/mysql.txt`,
- polecenie startu Gunicorn,
- instrukcję użycia przydzielonego portu i subdomeny `wykr.es`,
- kopię zapasową danych przez `mysqldump`,
- prosty health endpoint `/health`.

### Oczekiwane artefakty

1. Działający kod.
2. Testy zakończone sukcesem.
3. Seed demonstracyjny.
4. README po polsku.
5. Krótka dokumentacja architektury.
6. Diagram ERD w Mermaid.
7. Diagram przepływu procesu w Mermaid.
8. Tabela zgodności z siedmioma wymaganiami profesora.
9. Lista znanych ograniczeń.
10. Instrukcja demo na 5 minut.

### Zasady jakości

- nie usuwaj działających funkcji bez potrzeby,
- nie twórz fikcyjnych informacji o AHE,
- nie obiecuj punktów stypendialnych,
- nie zapisuj danych o niepełnosprawności użytkownika,
- nie umieszczaj sekretów w kodzie,
- nie kończ pracy na makietach — aplikacja ma działać,
- po każdej większej zmianie uruchamiaj testy,
- przed zakończeniem wykonaj self-review bezpieczeństwa i UX.

Najpierw pokaż plan wdrożenia i drzewo projektu. Następnie rozpocznij implementację bez zbędnego czekania na potwierdzenie.
