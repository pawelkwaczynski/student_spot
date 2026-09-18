# StudentSpot

<p align="center">
  <a href="README.md">🇬🇧 In English</a> ·
  <a href="#co-potrafi">Co potrafi</a> ·
  <a href="#uruchomienie-lokalne">Uruchomienie</a> ·
  <a href="#testy">Testy</a>
</p>

StudentSpot to otwarta platforma dla kół naukowych, dostępności kampusu i rezerwacji sal.
Pozwala kołu opublikować swój profil, przyjmować zgłoszenia członkowskie, wysyłać wiadomości,
szukać sal dostępnych architektonicznie, składać wnioski o rezerwację i eksportować zatwierdzone
spotkania do pliku kalendarza.

StudentSpot **nie jest oficjalnym systemem AHE**. Pokazuje, jak lekki system informacyjny może
wesprzeć koordynację na kampusie: z dostępnością, dwujęzycznym interfejsem i jasnym podziałem ról.

Nie ma obecnie publicznej instancji. Projekt jest do postawienia u siebie, a `Uruchomienie lokalne`
niżej stawia go trzema komendami.

## Po co to jest

Koła naukowe i studenci z potrzebami dostępności robią te same rzeczy w rozsypanych narzędziach:
zgłoszenie do koła przez formularz, rezerwacja sali mailem, informacja o dostępności w PDF na stronie,
kalendarz w trzecim miejscu. StudentSpot łączy to w jeden przepływ:

- przeglądanie kół naukowych i rekomendacji,
- składanie i rozpatrywanie zgłoszeń członkowskich,
- zarządzanie rolami w kole i komunikacja z członkami,
- wyszukiwanie sal po pojemności, wyposażeniu i wymaganiach dostępności,
- wniosek o salę z wykrywaniem kolizji terminów,
- zatwierdzanie i odrzucanie rezerwacji z historią statusów do audytu,
- eksport zatwierdzonych spotkań do pliku `.ics`,
- interfejs po polsku i angielsku, tryb ciemny, wysoki kontrast, powiększona czcionka.

## Co potrafi

- Sale ograniczone do budynku przy ul. Sterlinga 26.
- Interfejs PL i EN, tryb ciemny, wysoki kontrast, większa czcionka.
- Dwuetapowa rejestracja z aktywacją mailową, zgodami i wyborem koła.
- Zgłoszenia członkowskie oraz decyzje administratora i opiekuna.
- Katalog sal ze zdjęciami, filtrami, mapą budynku i dopasowaniem po pojemności.
- Katalog 7 publicznych kół AHE plus wpisy ukryte, czekające na potwierdzenie.
- Rezerwacje z wykrywaniem kolizji, decyzjami i historią statusów.
- Eksport zatwierdzonych spotkań do `.ics`.
- Strony `/news`, `/calendar`, `/local-heroes`, `/info` i `/media`.
- Wiadomości w aplikacji: opiekun pisze do przyjętych członków koła.
- Konta organizatorów UTW i ogłoszenia administratora.
- Powiadomienia w aplikacji i podstawowy dziennik zdarzeń.

## Plany

- Migracje Alembic pod długoterminowy rozwój schematu.
- Wysyłka maili z linkami aktywacyjnymi i powiadomieniami.
- Rezerwacje cykliczne i subskrypcja kalendarza.
- Bogatsze strony organizacji dla społeczności uczelnianych.
- Notatki z audytu WCAG i automatyczne testy dostępności.
- Punkty API o dostępności sal i danych kół.
- Przepisy wdrożeniowe na słaby VPS, Dockera i platformy zarządzane.

## Uruchomienie lokalne

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo   # dane wyłącznie deweloperskie i testowe
flask --app wsgi:app run --port 8000
```

Otwórz `http://127.0.0.1:8000`. Komenda `seed-demo` wypisuje hasło kont demonstracyjnych
wygenerowane na ten jeden przebieg; nie ma go w kodzie.

## Wdrożenie produkcyjne

Produkcja stoi na jednej bazie kanonicznej: MySQL skonfigurowany przez `DATABASE_URL` w `.env`
(wzór w `.env.example`). SQLite jest tylko lokalną wersją deweloperską.

```bash
flask --app wsgi:app init-db
flask --app wsgi:app seed-catalog                      # kierunki, koła, sale, bez kont
flask --app wsgi:app create-admin --email admin@example.com   # zapyta o hasło
gunicorn --workers 1 --threads 2 --timeout 60 --bind 0.0.0.0:${APP_PORT} wsgi:app
```

Szczegóły wdrożenia: `docs/FROG_DEPLOYMENT.md`.

## Testy

```bash
. .venv/bin/activate
python -m pytest
```

32 testy, wszystkie offline.

## Współpraca

Zgłoszenia są mile widziane. Dobre pierwsze obszary to dokumentacja, testy, poprawki dostępności,
tłumaczenia, dopracowanie interfejsu i drobne funkcje we Flasku i Jinja2.
Szczegóły: [CONTRIBUTING.md](CONTRIBUTING.md).

## Bezpieczeństwo

Proszę nie zgłaszać publicznie błędów bezpieczeństwa, jeśli zawierają szczegóły ataku, dane prywatne,
poświadczenia albo informacje o serwerze. Zgłoszenie prywatne: [SECURITY.md](SECURITY.md).

Zasady:

- hasła i tokeny aktywacyjne są hashowane,
- formularze mają ochronę CSRF,
- dane zaseedowane muszą pozostać fikcyjne,
- nie zbieramy prawdziwych diagnoz medycznych ani informacji o niepełnosprawności,
- kontrola dostępu jest egzekwowana po stronie serwera,
- `.env`, lokalne notatki dostępowe i poświadczenia nie trafiają do gita.

## Licencja

MIT. Copyright 2026 Paweł Kwaczyński.
