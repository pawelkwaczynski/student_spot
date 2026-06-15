# Schemat prezentacji ustnej StudentSpot - 10 minut

## Cel prezentacji

Pokazać StudentSpot jako prototyp systemu informatycznego wspierającego zarządzanie aktywnością kół naukowych AHE: rejestrację studentów, wybór koła, obsługę członkostwa, rezerwacje sal Sterlinga 26, decyzje administracyjne, komunikację i dostępność.

## Przygotowanie przed prezentacją

1. Uruchom aplikację lokalnie:

```bash
flask --app wsgi:app run --port 8000
```

2. Otwórz:

```text
http://127.0.0.1:8000
```

3. Przygotuj konto demo:

```text
guardian@studentspot.example.com
StudentSpot123!
```

W razie potrzeby pokaż też konto:

```text
boss@studentspot.example.com
StudentSpot123!
```

## Minuta 0:00-1:00 - wejście i problem

Ekran: `Start`

Co pokazać:

- stronę główną,
- logo i identyfikację AHE,
- sekcję sal, kół i aktualności.

Co powiedzieć:

StudentSpot rozwiązuje problem rozproszonej komunikacji w kołach naukowych. W jednym miejscu student może znaleźć koło, opiekun widzi członków, osoby uprawnione rezerwują sale, a administracja podejmuje decyzje i zostawia ślad audytowy.

## Minuta 1:00-2:00 - miejsce użycia i organizacja

Ekran: `/info`

Co pokazać:

- kontekst projektu,
- autora i afiliację,
- mapę wymagań projektowych,
- schemat organizacyjny.

Co powiedzieć:

Przyszłym miejscem użycia jest organizacja edukacyjna: AHE w Łodzi oraz środowisko kół naukowych. System obsługuje studentów, opiekunów kół, administrację sal, administrację systemu oraz organizatorów UTW.

## Minuta 2:00-3:00 - role i uprawnienia

Ekran: `/demo`

Co pokazać:

- konta demo,
- role użytkowników.

Co powiedzieć:

Role są rozdzielone. Student nie wybiera sam funkcji przewodniczącego ani zastępcy. Po rejestracji jest zwykłym studentem, a status i rolę w kole potwierdza opiekun lub administrator.

## Minuta 3:00-4:00 - rejestracja i wybór koła

Ekran: `/auth/register`

Co pokazać:

- krok 1: dane osobowe i studenckie,
- krok 2: bezpieczeństwo, hasło i zgody,
- listę kierunków zamiast pola dowolnego.

Co powiedzieć:

Rejestracja jest dwuetapowa. Konto po wysłaniu formularza trafia do statusu oczekującego na weryfikację e-maila. Po aktywacji student przechodzi do wyboru koła, a system może rekomendować koła powiązane z kierunkiem.

## Minuta 4:00-5:00 - katalog kół i Local Heroes

Ekrany: `/clubs`, `/local-heroes`

Co pokazać:

- katalog kół,
- filtrowanie,
- profile Local Heroes,
- dopasowanie Local Heroes do koła na koncie użytkownika.

Co powiedzieć:

Katalog kół zbiera informacje, które zwykle są rozproszone: opis, kierunki, opiekuna, tagi i sugerowane sale. Local Heroes pokazuje dodatkową warstwę komunikacyjną: osoby, które mogą inspirować studentów i wspierać identyfikację z uczelnią.

## Minuta 5:00-6:30 - moje konto i opiekun koła

Ekran: zaloguj `guardian@studentspot.example.com`, potem `/admin`

Co pokazać:

- listę wniosków członkowskich,
- pełną listę członków koła,
- zmianę roli,
- zatwierdzanie lub odrzucanie statusu,
- przycisk wysłania wiadomości.

Co powiedzieć:

Opiekun koła ma panel operacyjny. Widzi nie tylko oczekujące wnioski, ale też aktualną listę członków swojego koła. Może zatwierdzić status, zmienić rolę i wysłać wiadomość do wszystkich zatwierdzonych członków.

## Minuta 6:30-7:30 - wiadomości w aplikacji

Ekrany: `/messages/compose`, `/messages`

Co pokazać:

- formularz wiadomości opiekuna,
- skrzynkę odbiorczą,
- wiadomość po stronie członka.

Co powiedzieć:

Komunikacja jest wewnątrz aplikacji. Opiekun koła wysyła komunikat do członków, a członek widzi go w skrzynce. To ogranicza chaos mailowy i pozwala później rozbudować system o historię komunikacji.

## Minuta 7:30-8:30 - sale, rezerwacje i dostępność

Ekrany: `/rooms`, `/reservations/new`

Co pokazać:

- wyszukiwanie sal,
- dopasowanie po liczbie osób,
- zdjęcia sal i lightbox,
- formularz rezerwacji,
- wymagania dostępnościowe.

Co powiedzieć:

System dobiera sale do liczby uczestników i wyposażenia. Rezerwować mogą tylko osoby uprawnione, a system sprawdza konflikty terminów. W formularzu są też potrzeby organizacyjne dostępności, np. tłumacz języka migowego, przewodnik, transport z terenu Łodzi i sprzęt wspomagający dydaktykę.

## Minuta 8:30-9:15 - kalendarz, aktualności i dokumenty wynikowe

Ekrany: `/calendar`, `/news`, zatwierdzona rezerwacja z `.ics`

Co pokazać:

- kalendarz demonstracyjny czerwiec/lipiec 2026,
- feed aktualności,
- eksport spotkania do kalendarza.

Co powiedzieć:

Dokumenty wynikowe w prototypie są rekordami systemowymi: wniosek członkowski, wniosek rezerwacyjny, decyzja statusowa, powiadomienie, wpis audytu i plik kalendarza `.ics`.

## Minuta 9:15-10:00 - podsumowanie wymagań i technologia

Ekrany: `/info`, `/media`

Co pokazać:

- wymagania funkcjonalne i niefunkcjonalne,
- PL/EN,
- dark mode, kontrast, A+,
- sekcję Media z plikami.

Co powiedzieć:

Projekt spełnia wymagania: opisuje miejsce użycia, problem, role, założenia, funkcje, ograniczenia i przepływy informacyjne. Aplikacja działa jako prototyp webowy, ma dwie wersje językowe, tryb ciemny, wysoki kontrast, większą czcionkę i responsywny widok desktop/tablet/mobile.

## Plan awaryjny, gdy zostają tylko 3 minuty

1. Start: powiedz problem i cel.
2. Info: pokaż mapę wymagań projektowych.
3. Admin jako opiekun: pokaż członków i zatwierdzanie statusu.
4. Rezerwacja: pokaż formularz i dostępność.
5. Kalendarz: pokaż `.ics` i podsumuj dokumenty wynikowe.

## Najważniejsze zdania do zapamiętania

- StudentSpot porządkuje procesy kół naukowych: członkostwo, rezerwacje, komunikację i decyzje.
- Student nie nadaje sobie roli funkcyjnej samodzielnie; robi to opiekun albo administrator.
- Rezerwacje sal są ograniczone do budynku Sterlinga 26 i sprawdzają konflikty terminów.
- System wspiera dostępność organizacyjną wydarzeń.
- Aplikacja jest prototypem studenckim, ale pokazuje pełną logikę systemu zarządzania informacją.
