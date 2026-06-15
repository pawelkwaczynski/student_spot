# StudentSpot - postep prac

Ostatnia aktualizacja: 2026-06-14

## Aktualny status

- Zrealizowano aktualizacje z 17 punktow: wiekszy logotyp, bialy pasek naglowka, czytelniejsze tagi, powrot popupu welcome, przebudowany hero bez prawej grafiki, przycisk `UP`, klik w logo wraca na start.
- Dodano `/news` z 6 templatkami aktualnosci z `blog_package.zip`; paczka i rozpakowane pliki sa w `source_info/blog_package/`, grafiki skopiowane do `app/static/media/news/`.
- Dodano `/calendar` z demonstracyjnymi rezerwacjami sal na czerwiec i lipiec 2026.
- Dodano `/local-heroes` z profilami lokalnych liderow/ambasadorow/ekspertow AHE; sekcje ambasadorow usunieto z `/info` i `/media`.
- `/info`: "Mapa wymagan projektowych", gwiazdka dla UTW AHE, nowy opis KV ze zrodlem `view-source:https://www.ahe.lodz.pl//themes/custom/ahe/css/style.css`, model kont UTW przeniesiony z `/demo` na dol strony, grafika powieksza sie po kliknieciu.
- `/demo`: usunieto grafike, usunieto sekcje KV, usunieto model UTW; zostaly konta demo, opis projektu, tech stack i autor.
- `/media`: zostala notatka prasowa oraz 6 downloadow (StudentSpot, popup welcome, AHE PL/EN, Samorzad AHE, UTW AHE); usunieto autora, KV i downloady ambasadorow/ekspertow; grafiki powiekszaja sie po kliknieciu.
- `/rooms`: wyniki po `participants` sortuja sie po najlepszym dopasowaniu pojemnosci; karty pokazuja wolne miejsca; puste wyniki z filtrami wyposazenia/dostepnosci maja zaslepke o modernizacji danych.
- Rejestracja: dodano 2 kroki, `confirm_password`, `study_level`, `study_mode`, status `pending_verification`, znaczniki akceptacji regulaminu/RODO, `email_verified_at` po aktywacji i ekran `/auth/choose-club`.
- Model `users` rozszerzono o `study_level`, `study_mode`, `email_verified_at`, `terms_accepted_at`, `privacy_accepted_at`; dodano migracje `migrations/002_user_registration_fields.sql` i wykonano ja na lokalnej bazie SQLite.
- Usunieto z aplikacji stare ostrzezenia sugerujace kontekst medyczny; zostala neutralna informacja o potrzebach organizacyjnych wydarzenia.
- Utrzymano 8 kont demo, tylko sale Sterlinga 26, watermark `TEMPLATRE` dla K200A/K320, lightbox sal i grafik, PL/EN, dark mode, kontrast i A+.
- Weryfikacja automatyczna: `PYTHONPATH=. .venv/bin/python -m compileall app tests` OK, `PYTHONPATH=. .venv/bin/pytest -q` = 21 passed, `PYTHONPATH=. .venv/bin/python -m pip check` OK.
- Render QA przez Browser/IAB: 33 kombinacje stron i viewportow (desktop 1440x900, tablet 1024x768, telefon 390x844), zero poziomego overflow, zero uszkodzonych obrazkow, zero bledow konsoli aplikacji; header bialy, `/rooms` bez filtrow zaczyna od Aula A01, a `/rooms?participants=23` od najlepiej dopasowanej sali.
- Lokalny serwer do review dziala na `http://127.0.0.1:8000`.
- ZIP odtworzony: `student_spot.zip` ma ok. 34 MB i zawiera nowe trasy, migracje, grafiki newsow oraz `source_info/blog_package*`.
- Repo GitHub utworzone jako prywatne: `https://github.com/pawelkwaczynski/student_spot`; branch `main`, remote `origin`.
- Do wykonania po tej aktualizacji: reczny review uzytkownika przed Frog.

## Aktualny checkpoint do wznowienia

1. Zrobic reczny review lokalnie: `http://127.0.0.1:8000`.
2. Po akceptacji recznej przepakowac ZIP i wgrac `student_spot.zip` na Frog dopiero po potwierdzeniu oraz ustawic `.env` wedlug `docs/FROG_DEPLOYMENT.md`.

## Poprzedni status

- Przeczytano materialy startowe: README, specyfikacje MVP, dane/zrodla, prompt Codex, prompt Claude oraz dokument DOCX.
- Ustalono stack: Flask/Jinja2/SQLAlchemy/SQLite lokalnie/PyMySQL na Frog.
- Przyjeto zakres: kompletne MVP z PL/EN, dark mode, high contrast, wieksza czcionka, testami, dokumentacja i ZIP.
- Utworzono plan realizacji w `IMPLEMENTATION_PLAN.md`.
- Zmieniono zakres zgodnie z decyzja uzytkownika: tylko sale i budynek przy Sterlinga 26.
- Nowe zdjecia z `source_info/` skopiowano do `app/static/media/rooms/`.
- Seed demo ma miec 8 kont: `admin@studentspot.example.com`, `property@studentspot.example.com`, `guardian@studentspot.example.com`, `boss@studentspot.example.com`, `vice@studentspot.example.com`, `member@studentspot.example.com`, `pending@studentspot.example.com`, `utw@studentspot.example.com`, haslo `StudentSpot123!`.
- Nowe logo `source_info/logo.png` skopiowano do `app/static/media/brand/studentspot-logo.png` i podpieto w headerze.
- Testy `python -m pytest`: 10 passed.
- Smoke test Playwright: logo widoczne, zdjecia sal widoczne, dashboard boss dziala, mobile bez poziomego overflow.
- Utworzono finalna paczke `student_spot.zip`.

## Najblizszy krok

1. Wgrac `student_spot.zip` na Frog.
2. Na Frog ustawic `.env` wedlug `docs/FROG_DEPLOYMENT.md`.
3. Uruchomic `deploy_frog.sh` albo komendy z dokumentacji.

## Krytyczne wymagania do pilnowania

- Rezerwacje: konflikt czasu to `new_start < existing_end AND new_end > existing_start`.
- Rezerwowac moga tylko: `chair`, `vice_chair`, `club_guardian`, `utw_organizer`, `property_admin`, `system_admin`.
- Tokeny aktywacyjne i hasla nie moga byc zapisane jawnie.
- Brak prawdziwych sekretow w repo.
- Brak danych medycznych i brak pola `is_disabled` na uzytkowniku.
- Interfejs musi dzialac po polsku i angielsku.
- Dark mode, wysoki kontrast i wieksza czcionka musza byc dostepne od razu w UI.
- Nie dodawac sal spoza Sterlinga 26. G1/G2/Rewolucji usuniete z zakresu demo.

## Komendy weryfikacyjne do uruchamiania

```bash
python -m pytest
python -m compileall app tests
flask --app wsgi:app routes
```

## Wznowienie po przerwaniu

Zacznij od:

```bash
cd /Users/pawelkwaczynski/Desktop/student_spot
sed -n '1,220p' PROGRESS.md
find . -maxdepth 3 -type f | sort
python -m pytest
```

Nastepnie kontynuuj od pierwszego niezrobionego punktu w sekcji `Najblizszy krok` albo `Do zrobienia`.

## Do zrobienia

- [x] `source_info/` z materialami wejsciowymi.
- [x] Szkielet Flask.
- [x] Modele SQLAlchemy.
- [x] Seed demo dla Sterlinga i 8 kont demo.
- [x] Auth i aktywacja.
- [x] Czlonkostwa i role.
- [x] Sale i wyszukiwarka.
- [x] Rezerwacje i approval.
- [x] Dashboard i wydarzenia.
- [x] PL/EN.
- [x] Dark mode, high contrast, wieksza czcionka.
- [x] Testy.
- [x] Dokumentacja Frog.
- [x] ZIP finalny.
- [x] Zakladka Info z KV, autorem, mapa wymagan projektowych i modelem UTW.
- [x] Mapa wymagan projektowych w `/info`.
- [x] Zakladka Aktualnosci.
- [x] Zakladka Kalendarz.
- [x] Zakladka Local Heroes.
- [x] Rejestracja 2-krokowa i ekran wyboru kola.
- [x] QA responsywnosci desktop/tablet/telefon.

## Wyniki ostatniej weryfikacji

Aktualizacja UI z 2026-06-15:
- Podmieniono aktywne tlo aplikacji na `app/static/media/visuals/background-new.png` z `source_info/background_new.png`.
- Powiekszono logotyp StudentSpot w naglowku i poprawiono responsive header, zeby `Media` nie spadalo samotnie do kolejnego rzedu.
- Dodano `Zarejestruj sie` obok `Zaloguj sie` w pasku gornym.
- Przycisk `UP` przeniesiono na biale tlo nad stopka i dodano strzalke.
- Popup powitalny startuje automatycznie na stronie glownej.
- Strona glowna nie pokazuje juz przyciskow `Sale` i `Demo` w sekcji hero.
- Browser QA: 2048, 1440, 1024 i 390 px bez poziomego overflow; nowe tlo aktywne.

```bash
python -m compileall app tests
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo
flask --app wsgi:app routes
python -m pytest
bash scripts/package_release.sh
```

Wynik ostatni: `21 passed`. ZIP `student_spot.zip` zostal przepakowany po zmianach z 17 punktow.
