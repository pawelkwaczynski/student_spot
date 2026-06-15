# StudentSpot - postep prac

Ostatnia aktualizacja: 2026-06-15

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

1. Aktualne zmiany sa po testach lokalnych: `compileall`, `pytest`, `pip check`, `flask routes` oraz Browser QA kluczowych ekranow.
2. Przepakowac ZIP-y komendami: `bash scripts/package_release.sh`, `bash scripts/package_professor_release.sh`, `bash scripts/package_dev_handoff.sh`.
3. Ostatni deploy Frog dziala pod adresem `https://frog01-20412.wykr.es`; po kolejnych zmianach powtorzyc commit, push i deploy z paczki profesorskiej.

## Poprzedni status

- Przeczytano materialy startowe: README, specyfikacje MVP, dane/zrodla oraz dokument DOCX.
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
- Aktualizacja brandingu: usunieto osobny napis `StudentSpot` z naglowka, powiekszono graficzne logo aplikacji, dodano logo StudentSpot + AHE w bialej stopce.
- Aktualizacja stopki i zakladek: logotypy w stopce sa po prawej, AHE zmniejszone, `2026` pogrubione, stopka trzyma tekst w jednej linii na desktopie.
- Dodano logotypy 7 kol naukowych: AIrON, Kognitywistyczno-Eksperymentalne, Grafika, Arteterapeutyczne Warsztaty Emocji, Progressus, Wkreceni, Pedagogika Dziecka. Logo AIrON przyciete z kwadratu do prostokata.
- Ujednolicono uklad zakladek: tytuly `Info`, `Media`, `Demo`, `Aktualnosci`, `Kalendarz`, `Local Heroes`, szczegoly kola i rezerwacji sa nad panelem, nie w szarym tle.

Aktualizacja oddaniowa z 2026-06-15:
- W rezerwacji sal dodano cztery potrzeby organizacyjne dostępności: tłumacz języka migowego, przewodnik dla osoby niewidomej, bezpłatny transport z Łodzi i użyczenie sprzętu wspomagającego dydaktykę.
- Zmieniono nazewnictwo UTW na neutralny "komunikat do UTW" w UI, testach i dokumentacji.
- Dodano `docs/ODDANIE_PROJEKTU.md` z opisem dla profesora, GitHubem, instrukcją lokalną, Frog bez haseł oraz kontami demo.
- Dodano `scripts/package_professor_release.sh`; skrypt pomija prywatne notatki, `.env`, cache, bazę lokalną i robocze checkpointy.
- Usunięto z `source_info/` robocze pliki startowe i wyczyszczono checkpoint ze śladów narzędzi.
- Weryfikacja: `compileall` OK, `pytest` = 23 passed, Browser QA formularza rezerwacji i panelu admina bez błędów konsoli.
- Przycięto aktywne logo StudentSpot z kwadratu do prostokata i zmieniono CSS tak, zeby header oraz stopka nie wymuszaly pustej kwadratowej przestrzeni.
- Przycięto logo kola Kognitywistyczno-Eksperymentalnego do samego znaku kola, bez czerwonych podpisow i bez drugiego logo z zarowka.
- Browser QA po poprawce: desktop 1440 px bez poziomego overflow, header zredukowany z 193 px do 102 px, menu zostaje w jednej linii.
- Dopasowano hero strony glownej do tresci: panel ma taka sama szerokosc jak pasek trzech logotypow pod spodem i nie ma juz sztucznej wysokosci prawie calego ekranu.
- Ponownie przycięto logo Kognitywistyczno-Eksperymentalnego zgodnie ze screenem referencyjnym: sam ptak, nazwa i podpis `Kolo Naukowe`.
- Odchudzono header desktopowy: logo, menu i kontrolki sa w jednej linii, z mniejszym paddingiem i nizsza belka.
- Pasek `UP` ma szare tlo, a stopka jest nizsza; logotypy StudentSpot i AHE sa wieksze oraz wyrownane do tej samej wysokosci.
- Dodano popup EN jako `app/static/media/visuals/welcome-popup-en.png`; strona glowna, `Info` i `Media` wybieraja grafike popupu zgodnie z jezykiem.
- Logo Arteterapii i Pedagogiki Dziecka ustawiono jako kwadratowe 280x280, a `Koło Naukowe Pedagogiki Dziecka` przesunieto na koniec publicznej listy kol.
- Poprawiono kontrast dark mode: hero strony glownej, przycisk `Pokaz popup`, naglowki sekcji i tabele demo nie maja juz jasnego tekstu na jasnym tle. Browser QA: hero lead 9.54:1, `Pokaz popup` 15.98:1, tabela demo 9.54-15.98:1, bez poziomego overflow.
- Zmniejszono logotypy StudentSpot i AHE w stopce o ok. 30%; Browser QA `/clubs/`: oba logo 54 px wysokosci, jedna linia, brak poziomego overflow.
- Zmieniono stopke na `Projekt studencki: StudentSpot...` oraz dodano w `/info` zdanie o opiece prof. dr hab. Mariana Niedzwiedzinskiego i przedmiocie projektu; Browser QA potwierdzil teksty i brak overflow.
- Przebudowano `/local-heroes` wedlug referencji: 23 profile z nowo dodanych portretow i danych `source_info/ahe-2026-06-15.json`, duzy uklad portret + opis, bez starych placeholderow ikon. Browser QA: pierwszy profil `Adrian Makoć`, 23 profile, obrazy laduja sie, brak overflow; Playwright screenshot desktop/mobile.
- Cleanup po poprawkach: usunieto martwy CSS starego ukladu Local Heroes, stare placeholdery `ambassador-icon.png` / `expert-icon.png`, martwe klucze tlumaczen po sekcji ambasadorow oraz lokalne cache/duplikaty ZIP. Finalny ZIP wyklucza `student_spot*.zip`.
- Konto uzytkownika: `Dashboard` zmieniono na `Moje konto` / `My account`; konto pokazuje avatar, edycje danych, opcjonalny nick, zmiane hasla oraz sekcje filtrowane po wybranym kole.
- Po wyborze/posiadaniu kola konto pokazuje tylko sale, aktualnosci i Local Heroes dopasowane do tego kola. Dla konta `boss@studentspot.example.com` widac AIrON, sale K200A/K320, newsy AIrON i Błażeja Strusa.
- Rezerwacja sal pokazuje modal i note: sale moze rezerwowac tylko osoba uprawniona; backend nadal blokuje konta bez uprawnien.
- Rejestracja: nick jest opcjonalny, a przycisk `Dalej` w kroku 1 jest wyrownany do prawej.
- Local Heroes: pierwszy profil ustawiono na `Błażej Strus`, uklad powiekszono do referencji z portretem po lewej i trescia po prawej.
- Browser QA 2026-06-15: `/dashboard`, `/auth/profile`, `/auth/register`, `/reservations/new`, `/local-heroes`; desktop 1440 px i mobile 390 px bez poziomego overflow. Modal rezerwacji widoczny i zamykalny.
- Strona glowna ma feed aktualnosci pod sekcja kol; lead korzysta ze wspolnego klucza PL/EN.
- Local Heroes: opis wprowadzajacy jest rozbity na osobne linie, zgodnie z prosba uzytkownika.
- Dodano modul wiadomosci: opiekun kola/system admin moze wyslac wiadomosc do wszystkich zatwierdzonych czlonkow wybranego kola, czlonek widzi skrzynke `/messages`, odczyt oznacza wiadomosc jako przeczytana, a powiadomienia i audyt sa zapisywane.
- Panel opiekuna/admina ma pelna liste czlonkow kol, nie tylko oczekujace wnioski; opiekun moze zatwierdzic status i zmienic role czlonka w obrebie swoich kol.
- Zmieniono tekst dostepnosci transportu na `Zorganizowanie bezplatnego transportu z terenu Lodzi` / `Arrange free transport from the Lodz area`.
- Dodano `prezentacja_ustna_10_min.md` z kolejnoscia ekranow i tekstem do prezentacji przed profesorem.
- Weryfikacja jednostkowa/integracyjna: `.venv/bin/python -m pytest tests/test_core_flows.py` = 26 passed.
- Browser QA po module wiadomosci: strona glowna desktop 1440 px ma feed aktualnosci pod kolami i brak overflow; panel opiekuna pokazuje pelna liste czlonkow, role i przycisk wiadomosci; wysylka wiadomosci z konta opiekuna do AIrON trafia do skrzynki konta `boss`; mobile 390 px dla `/`, `/messages/`, `/local-heroes`, `/reservations/new` bez poziomego overflow.
- Finalna weryfikacja: `.venv/bin/python -m compileall app tests`, `.venv/bin/python -m pytest`, reset i seed demo, `bash scripts/package_release.sh`, `bash scripts/package_professor_release.sh`.
- Odtworzono `student_spot.zip` i `student_spot_profesor.zip` po aktualnych zmianach. ZIP profesorski wyklucza `.venv`, cache, lokalna baze, `.env`, `PROGRESS.md`, `IMPLEMENTATION_PLAN.md`, prywatne notatki i stare ZIP-y.

```bash
python -m compileall app tests
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo
flask --app wsgi:app routes
python -m pytest
bash scripts/package_release.sh
```

Wynik ostatni: `27 passed`. ZIP `student_spot.zip` oraz `student_spot_profesor.zip` sa przepakowane po aktualnych zmianach wiadomosci i panelu opiekuna.

Finalizacja oddaniowa 2026-06-15:
- Punkt `Status danych: active_verified` zostal pominiety jako omylkowy; publiczna lista kol nie pokazuje juz technicznego statusu danych.
- Strona glowna pokazuje 7 publicznych kol, lead w hero trzyma jedna linie na desktopie, a logo w stopce linkuja: StudentSpot do strony glownej, AHE do `https://www.ahe.lodz.pl/`.
- Plan budynku Sterlinga 26 otwiera sie w kompaktowym lightboxie z przyciskiem zamkniecia, tak jak pozostale powiekszane grafiki.
- `/demo` ma krotki tutorial pokazowy i rozpiske, co pokazac na kazdym koncie demo.
- Seed demo dodaje dodatkowych fikcyjnych czlonkow i wnioski, zeby opiekun mogl pokazac liste czlonkow, zatwierdzanie, zmiane rol oraz wysylke wiadomosci.
- Panel property admin nie pokazuje zarzadzania czlonkami; panel opiekuna i system admina pokazuje czlonkow i wnioski.
- Popup welcome startuje automatycznie tylko na stronie glownej, dzieki czemu nie przykrywa logowania.
- Dodano `scripts/package_dev_handoff.sh` i `plan_pokazowy_student_spot.md`; paczka handoff ma materialy do zachowania spojnosci kolejnych aplikacji AHE.
- Weryfikacja: `.venv/bin/python -m compileall app tests` OK, `.venv/bin/python -m pytest` = 27 passed, `.venv/bin/python -m pip check` OK, `.venv/bin/flask --app wsgi:app routes` OK.
- Browser QA: rezerwacja po zalogowaniu PL/EN pokazuje tekst o zatwierdzonym przedstawicielu kola, stary tekst `boss lub vice` nie wystepuje, formularz nie ma poziomego overflow, popup nie pokazuje sie automatycznie na logowaniu.
- GitHub: `main` wypchniety do `https://github.com/pawelkwaczynski/student_spot`, commit `85190eb`.
- Frog: aplikacja uruchomiona przez Gunicorn na porcie `20412`, publiczny adres `https://frog01-20412.wykr.es`, health check zwraca `{"service":"studentspot","status":"ok"}`.
- Publiczny Browser QA: home ma popup, 7 publicznych kol i brak overflow; logowanie `guardian@studentspot.example.com` dziala; panel opiekuna pokazuje czlonkow i przycisk wiadomosci.

Aktualizacja copy demo 2026-06-16:
- Zmieniono sekcje `Szybki tutorial pokazowy` w `/demo` na copy przekazane przez uzytkownika.
- Uspojniono wersje EN: `Quick demo tutorial` i `Suggested workflow`.
- Testy: `.venv/bin/python -m compileall app tests`, `.venv/bin/python -m pytest tests/test_core_flows.py`, `.venv/bin/python -m pip check` OK, `27 passed`.
- Browser QA `/demo` PL/EN: nowe copy widoczne, stare `Efekt wow` / `Strong demo path` usuniete, brak poziomego overflow.
