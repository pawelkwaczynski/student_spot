# StudentSpot — finalna specyfikacja MVP

## 1. Nazwa i definicja projektu

**StudentSpot** to dwujęzyczna aplikacja webowa wspierająca zarządzanie aktywnością kół naukowych, organizacji akademickich oraz rezerwacją sal na potrzeby spotkań, warsztatów, prezentacji i wydarzeń.

System ma umożliwić studentowi odnalezienie koła naukowego, zgłoszenie członkostwa, przeglądanie wydarzeń oraz — po uzyskaniu odpowiedniej roli — złożenie wniosku o rezerwację sali. Administracja uczelni otrzymuje prosty panel do zatwierdzania lub odrzucania rezerwacji.

## 2. Miejsce przyszłego użytkowania

### Organizacja

Akademia Humanistyczno-Ekonomiczna w Łodzi oraz działające przy niej:

- koła naukowe,
- Samorząd Studentów,
- organizatorzy wydarzeń akademickich,
- Uniwersytet Trzeciego Wieku,
- Dział Obsługi Nieruchomości,
- Biuro / Rzecznik ds. osób z niepełnosprawnościami.

### Uproszczony schemat organizacyjny

```text
AHE
├── Władze i dziekani kierunków
├── Dział Obsługi Nieruchomości
│   └── zatwierdzanie i obsługa rezerwacji sal
├── Rzecznik ds. osób z niepełnosprawnościami
│   └── konsultacja dostępności i wsparcia
├── Samorząd Studentów
├── Uniwersytet Trzeciego Wieku
└── Koła naukowe
    ├── opiekun koła
    ├── przewodniczący
    ├── wiceprzewodniczący
    ├── sekretarz
    ├── skarbnik
    └── członkowie
```

## 3. Problem do rozwiązania

Obecnie informacje o kołach, ich spotkaniach, salach i procedurach mogą być rozproszone pomiędzy stronami internetowymi, pocztą elektroniczną, formularzami i komunikatorami.

Najważniejsze problemy:

- trudność w znalezieniu koła odpowiadającego kierunkowi studiów,
- brak jednego miejsca z informacją o wydarzeniach koła,
- ręczna obsługa zgłoszeń członkostwa,
- ryzyko kolizji rezerwacji sal,
- brak jednolitego procesu zatwierdzania,
- brak łatwego filtrowania sal według pojemności i wyposażenia,
- niedostateczne uwzględnianie potrzeb dostępnościowych,
- brak przejrzystej historii decyzji i zmian statusów.

## 4. Cel systemu

Celem StudentSpot jest uporządkowanie przepływu informacji między studentami, władzami kół oraz administracją obiektu.

System ma:

1. centralizować informacje o kołach i wydarzeniach,
2. wspierać proces dołączania do koła,
3. rekomendować sale odpowiednie do wydarzenia,
4. zapobiegać konfliktom terminów,
5. obsługiwać akceptację rezerwacji,
6. informować o statusie wniosku,
7. uwzględniać wymagania dostępności bez gromadzenia diagnoz medycznych,
8. zapewniać historię operacji i podstawowy audyt.

## 5. Zakres MVP

### Funkcje obowiązkowe

- ekran powitalny,
- wybór języka polskiego lub angielskiego,
- rejestracja studenta,
- aktywacja konta kodem lub linkiem e-mail,
- logowanie i wylogowanie,
- edycja profilu,
- katalog kierunków,
- katalog kół naukowych,
- dopasowanie kół do kierunków,
- wniosek o członkostwo,
- potwierdzanie członkostwa przez opiekuna lub administratora,
- role w kole,
- katalog sal,
- filtrowanie sal,
- tworzenie rezerwacji,
- wykrywanie konfliktów czasowych,
- akceptacja lub odrzucenie rezerwacji,
- historia statusów,
- wydarzenia i nadchodzące spotkania,
- powiadomienia w aplikacji,
- e-mail o aktywacji oraz zmianie statusu rezerwacji,
- panel administratora,
- podstawowy dziennik audytowy.

### Funkcje opcjonalne po MVP

- eksport rezerwacji do CSV,
- plik ICS do kalendarza,
- lista obecności,
- ocena spotkania,
- wypożyczanie sprzętu dostępnościowego,
- integracja z SSO / Keycloak,
- integracja z systemem dziekanatowym,
- moduł rekomendacji AI.

## 6. Użytkownicy i role

### Role globalne

#### Gość

- przegląda stronę startową,
- widzi ogólny katalog kół i publicznych wydarzeń,
- może rozpocząć rejestrację.

#### Student

- zarządza swoim profilem,
- wybiera koło,
- składa wniosek o członkostwo,
- widzi wydarzenia kół, do których należy,
- nie może rezerwować sal bez odpowiedniej roli.

#### Opiekun koła

- zatwierdza lub odrzuca członkostwo,
- przypisuje role w kole,
- przegląda rezerwacje koła,
- może potwierdzać zgodność wydarzenia z działalnością koła.

#### Administrator nieruchomości

- zarządza salami,
- ustawia wyłączenia sal,
- zatwierdza i odrzuca rezerwacje,
- podaje powód decyzji,
- przegląda kalendarz wszystkich rezerwacji.

#### Administrator systemu

- zarządza użytkownikami i słownikami,
- zarządza kierunkami i kołami,
- przegląda logi audytowe,
- nie powinien zmieniać danych bez pozostawienia śladu w audycie.

#### Organizator UTW

- konto tworzone przez administratora,
- widzi katalog sal i wydarzeń,
- może składać wnioski dla Uniwersytetu Trzeciego Wieku,
- nie wymaga numeru indeksu.

### Role w kole

- `chair` — przewodniczący,
- `vice_chair` — wiceprzewodniczący,
- `secretary` — sekretarz,
- `treasurer` — skarbnik,
- `member` — członek.

Uprawnienie do składania rezerwacji mają wyłącznie:

- przewodniczący,
- wiceprzewodniczący,
- opiekun koła,
- organizator UTW,
- administrator.

## 7. Rejestracja i aktywacja konta

### Typy kont

#### Student

Pola wymagane:

- numer indeksu: dokładnie 6 cyfr,
- imię,
- nazwisko,
- nick,
- e-mail,
- hasło,
- rok studiów,
- kierunek studiów,
- akceptacja regulaminu,
- potwierdzenie zapoznania się z informacją o prywatności.

Walidacja:

- indeks jest unikalny,
- e-mail jest unikalny,
- nick jest unikalny,
- hasło ma co najmniej 12 znaków,
- kierunek pochodzi wyłącznie ze słownika systemowego,
- rok studiów jest poprawny dla wybranego poziomu.

#### Organizator UTW / pracownik

- konta nie są samodzielnie rejestrowane,
- zakłada je administrator,
- numer indeksu nie jest wymagany.

### Aktywacja

1. System tworzy konto jako `pending_verification`.
2. Generuje jednorazowy kod z ograniczonym czasem ważności.
3. Wysyła kod lub link na e-mail.
4. Po poprawnej weryfikacji ustawia status `active`.
5. Kod nie może być przechowywany w bazie w postaci jawnej.

### Tryb demonstracyjny

Jeżeli SMTP nie jest skonfigurowane:

- system zapisuje kod aktywacyjny w logu aplikacji,
- na środowisku developerskim pokazuje bezpieczny komunikat testowy,
- tryb ten musi być wyłączony w produkcji.

## 8. Onboarding do koła naukowego

Po aktywacji konta:

1. System odczytuje kierunek użytkownika.
2. Wyświetla koła przypisane do kierunku.
3. Użytkownik wybiera jedno z działań:
   - „Jestem członkiem”,
   - „Chcę dołączyć”,
   - „Nie znalazłem koła”.
4. Każde zgłoszenie trafia do statusu `pending`.
5. Opiekun lub administrator zatwierdza członkostwo.
6. Dopiero po zatwierdzeniu użytkownik widzi treści wewnętrzne koła.

### Brak koła dla kierunku

System pokazuje:

- informację, że student może zainicjować nowe koło,
- korzyści z działalności naukowej i projektowej,
- odnośnik do oficjalnej strony kierunku,
- kontakt do dziekana pobierany ze słownika administracyjnego,
- przycisk „Przygotuj zgłoszenie utworzenia koła”.

Nie wolno obiecywać konkretnych punktów stypendialnych lub ECTS bez potwierdzonego regulaminu. Tekst ma mówić o potencjalnych korzyściach: portfolio, networking, doświadczenie projektowe, konferencje, konkursy i rozwój kompetencji.

## 9. Dashboard po zalogowaniu

Dashboard pokazuje:

- najbliższe spotkanie użytkownika,
- liczbę nadchodzących spotkań,
- status zgłoszeń członkostwa,
- status ostatniej rezerwacji,
- skrót wydarzeń koła,
- przycisk rezerwacji — tylko dla uprawnionych,
- skrót profilu i roli,
- sekcję „Potrzebujesz dostępnej sali?”.

## 10. Katalog sal

Każda sala ma:

- nazwę,
- kod,
- budynek,
- piętro,
- pojemność,
- typ,
- opis PL i EN,
- zdjęcie,
- adres,
- wskazówkę lokalizacyjną,
- link do mapy budynku,
- listę wyposażenia,
- informację o dostępności,
- status aktywna / wyłączona.

### Cechy wyposażenia

- projektor,
- ekran,
- nagłośnienie,
- mikrofon,
- komputery,
- Wi-Fi,
- tablica,
- flipchart,
- klimatyzacja,
- scena / podest,
- pętla indukcyjna.

### Cechy dostępności

- dostęp windą,
- dostęp bezstopniowy,
- toaleta dostępna,
- szerokie przejścia,
- pętla indukcyjna,
- stanowiska komputerowe dostosowane,
- możliwość wsparcia tłumacza PJM,
- możliwość dodatkowej konsultacji z rzecznikiem.

System nie zapisuje informacji typu „użytkownik jest osobą z niepełnosprawnością”. W formularzu rezerwacji zapisuje jedynie wymagania organizacyjne danego wydarzenia.

## 11. Wyszukiwanie sal

Filtry:

- data,
- godzina rozpoczęcia,
- godzina zakończenia,
- liczba osób,
- komputery,
- projektor,
- nagłośnienie,
- pętla indukcyjna,
- dostęp windą,
- bezstopniowy dostęp,
- budynek.

### Logika dopasowania

Sala jest rekomendowana, jeżeli:

- ma odpowiednią pojemność,
- posiada wszystkie wymagane cechy,
- nie jest wyłączona,
- nie koliduje z zatwierdzoną ani oczekującą rezerwacją,
- spełnia wskazane wymagania dostępności.

Wyniki są sortowane:

1. pełne dopasowanie,
2. najmniejszy niewykorzystany zapas pojemności,
3. liczba dodatkowych udogodnień.

## 12. Rezerwacja

Pola wymagane:

- organizacja / koło,
- sala,
- tytuł spotkania,
- opis spotkania,
- data,
- godzina od,
- godzina do,
- przewidywana liczba osób,
- typ wydarzenia,
- wymagane wyposażenie,
- wymagania dostępnościowe.

### Statusy

- `draft`,
- `pending`,
- `approved`,
- `rejected`,
- `cancelled`,
- `completed`.

### Reguły

- czas zakończenia musi być późniejszy niż rozpoczęcia,
- rezerwacja nie może dotyczyć przeszłości,
- liczba uczestników nie może przekraczać pojemności sali,
- tylko uprawniona osoba może wysłać wniosek,
- konflikt blokuje wysłanie wniosku,
- odrzucenie wymaga uzasadnienia,
- każda zmiana statusu trafia do historii.

## 13. Panel administratora nieruchomości

Widoki:

- kolejka oczekujących wniosków,
- kalendarz dzienny i tygodniowy,
- szczegóły wniosku,
- lista konfliktów,
- zarządzanie salami,
- blokady techniczne sal,
- raport liczby rezerwacji.

Działania:

- zatwierdź,
- odrzuć z powodem,
- poproś o korektę,
- anuluj z uzasadnieniem,
- ustaw niedostępność sali.

## 14. Wydarzenia i spotkania

Zatwierdzona rezerwacja może automatycznie utworzyć wydarzenie koła.

Wydarzenie ma:

- tytuł,
- opis,
- datę i godzinę,
- salę,
- organizatora,
- widoczność: publiczna / tylko członkowie,
- liczbę planowanych uczestników,
- informację o dostępności.

## 15. Powiadomienia

### W aplikacji

- aktywacja konta,
- decyzja o członkostwie,
- złożenie rezerwacji,
- zmiana statusu,
- przypomnienie o wydarzeniu,
- anulowanie rezerwacji.

### E-mail

Minimum:

- kod aktywacyjny,
- zatwierdzenie / odrzucenie członkostwa,
- zatwierdzenie / odrzucenie rezerwacji.

## 16. Audyt

Rejestrowane zdarzenia:

- logowanie poprawne i niepoprawne,
- aktywacja konta,
- zmiana roli,
- zatwierdzenie członkostwa,
- utworzenie i edycja rezerwacji,
- zmiana statusu rezerwacji,
- edycja sali,
- administracyjna zmiana danych użytkownika.

Log zawiera:

- użytkownika,
- typ akcji,
- typ i identyfikator obiektu,
- datę,
- adres IP po anonimizacji lub skróceniu,
- metadane bez danych wrażliwych.

## 17. Model danych

### Główne tabele

- `users`
- `email_verification_tokens`
- `majors`
- `organizations`
- `clubs`
- `club_major_links`
- `club_memberships`
- `rooms`
- `room_features`
- `room_feature_links`
- `room_unavailability`
- `reservations`
- `reservation_required_features`
- `reservation_status_history`
- `events`
- `notifications`
- `audit_logs`
- `translations`

### Najważniejsze relacje

```text
users 1---N club_memberships N---1 clubs
majors N---N clubs
clubs 1---N reservations
rooms 1---N reservations
reservations 1---N reservation_status_history
rooms N---N room_features
reservations N---N room_features
reservations 0..1---1 events
```

## 18. Architektura techniczna

### Stack zalecany dla Frog

- Python,
- Flask,
- Jinja2,
- SQLAlchemy,
- MySQL przez `PyMySQL`,
- Flask-WTF / CSRF,
- Gunicorn: 1 worker, 2 threads,
- HTML + lokalny CSS,
- minimalny JavaScript bez frameworka SPA.

### Środowiska

- lokalne: SQLite lub MySQL,
- produkcyjne Frog: współdzielony MySQL,
- sekrety wyłącznie w zmiennych środowiskowych.

### Dlaczego bez Reacta i Keycloaka

Mikrus Frog oferuje 256 MB RAM i 3 GB dysku, dlatego MVP powinno być serwerowo renderowane i możliwie lekkie. Zewnętrzny Keycloak może być przyszłym rozszerzeniem, ale nie jest wymagany do zaliczeniowego MVP.

## 19. Wymagania niefunkcjonalne

### Bezpieczeństwo

- hasła hashowane bezpiecznym algorytmem,
- CSRF,
- walidacja danych po stronie serwera,
- kontrola uprawnień na każdej trasie,
- bezpieczne cookie sesji,
- limit prób logowania,
- brak sekretów w repozytorium,
- ochrona przed SQL injection przez ORM,
- logi bez haseł, tokenów i pełnych danych osobowych.

### Dostępność

Cel: zgodność z WCAG 2.1 AA w zakresie realnym dla MVP.

- pełna obsługa klawiaturą,
- widoczny focus,
- poprawne etykiety formularzy,
- komunikaty błędów powiązane z polami,
- wysoki kontrast,
- tekst alternatywny zdjęć,
- poprawna hierarchia nagłówków,
- `lang="pl"` / `lang="en"`,
- brak przekazywania znaczenia wyłącznie kolorem.

### Wydajność

- czas odpowiedzi zwykle poniżej 1 s dla danych demonstracyjnych,
- paginacja list administracyjnych,
- indeksy na datach, statusach i kluczach obcych,
- skompresowane obrazy WebP,
- brak ciężkich bibliotek front-endowych.

### Utrzymywalność

- podział na moduły / blueprints,
- konfiguracja przez `.env`,
- testy jednostkowe i integracyjne,
- dane startowe przez seed,
- dokumentacja README.

## 20. Dwujęzyczność

Interfejs PL / EN.

W MVP użyć prostego słownika tłumaczeń w plikach JSON lub Python, np.:

```text
translations/pl.json
translations/en.json
```

Treści dynamiczne, takie jak opis sali i koła, mają osobne pola PL i EN.

## 21. Projekt wizualny

### Styl

- zgodność wizualna z serwisem AHE,
- dużo bieli,
- czytelna typografia,
- czerwony jako akcent,
- granat / grafit dla tekstu,
- duże karty sal i wydarzeń,
- fotografia jako wsparcie, nie tło pod długi tekst.

### Zasady marki

- pobierać logotypy wyłącznie z oficjalnej sekcji AHE,
- nie deformować logotypów,
- nie zmieniać kolorów logotypów,
- nie udawać oficjalnego systemu,
- w stopce dodać: „Nieoficjalny projekt studencki”.

### Font

Agent ma sprawdzić font używany na stronie AHE. Jeżeli licencja lub dostępność nie pozwala go osadzić, użyć systemowego stacku:

```css
font-family: Inter, Arial, Helvetica, sans-serif;
```

## 22. Dane demonstracyjne

Utworzyć:

- 1 administratora systemu,
- 1 administratora nieruchomości,
- 1 opiekuna koła,
- 1 przewodniczącego,
- 1 wiceprzewodniczącego,
- 2 członków,
- 1 organizatora UTW,
- 5–8 sal,
- minimum 5 kół,
- 4 wydarzenia,
- rezerwacje w każdym kluczowym statusie.

Nie używać danych prawdziwych studentów jako kont testowych.

## 23. Testy akceptacyjne

Aplikacja jest gotowa do zaliczenia, gdy:

1. Student może założyć konto z walidacją wszystkich pól.
2. Nie można utworzyć drugiego konta z tym samym indeksem lub e-mailem.
3. Konto wymaga aktywacji.
4. Student może złożyć wniosek o członkostwo.
5. Opiekun może zatwierdzić członkostwo.
6. Zwykły członek nie widzi formularza rezerwacji.
7. Przewodniczący może wyszukać salę.
8. Filtr pojemności i wyposażenia działa poprawnie.
9. System wykrywa konflikt terminów.
10. Administrator może zatwierdzić lub odrzucić wniosek.
11. Odrzucenie wymaga powodu.
12. Zmiana statusu jest widoczna w historii.
13. Zatwierdzone wydarzenie pojawia się na dashboardzie.
14. Wymagania dostępności filtrują sale.
15. Przełączenie PL / EN zmienia interfejs.
16. Widoki nieuprawnione zwracają 403 lub przekierowanie.
17. Testy automatyczne przechodzą.
18. Aplikacja działa na publicznym adresie Froga.

## 24. Wdrożenie na Mikrus Frog

Frog ma ograniczone zasoby, więc:

- użyć współdzielonego MySQL,
- uruchomić Gunicorn z 1 workerem,
- aplikacja słucha HTTP na przydzielonym porcie,
- publiczny HTTPS zapewnia subdomena `wykr.es`,
- nie uruchamiać lokalnego MySQL, Redis, Dockera ani Keycloaka,
- obrazy ograniczyć do rozsądnego rozmiaru,
- dodać skrypt `deploy_frog.sh` i usługę startową OpenRC lub prosty proces nadzorowany.

Przykład uruchomienia:

```bash
gunicorn --workers 1 --threads 2 --bind 0.0.0.0:${APP_PORT} wsgi:app
```

## 25. Dokumenty wynikowe systemu

- potwierdzenie aktywacji konta,
- zgłoszenie członkostwa,
- decyzja o członkostwie,
- wniosek o rezerwację,
- decyzja o rezerwacji,
- kalendarz wydarzeń,
- historia statusów,
- raport rezerwacji według sali, koła i okresu,
- dziennik audytowy.

## 26. Przepływ informacji

```text
Student
  ↓ rejestracja i aktywacja
Profil
  ↓ wybór koła
Wniosek członkowski
  ↓ decyzja opiekuna
Członkostwo i rola
  ↓ przewodniczący / zastępca
Kryteria spotkania
  ↓ filtr sal i kontrola konfliktów
Wniosek rezerwacyjny
  ↓ administrator nieruchomości
Decyzja
  ↓
Powiadomienie + wydarzenie + historia audytowa
```

## 27. Poziom wykonania wymagany na ocenę 5

- działająca aplikacja online,
- spójny i estetyczny interfejs,
- role i uprawnienia,
- rzeczywisty workflow akceptacji,
- walidacja konfliktów,
- uwzględnienie dostępności,
- dwujęzyczność,
- dane demonstracyjne,
- testy,
- diagram bazy i architektury,
- instrukcja instalacji,
- opis zgodności z siedmioma punktami projektu profesora.
