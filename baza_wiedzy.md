# Baza wiedzy dla kolejnych aplikacji AHE Łódź

Ten dokument zbiera decyzje, problemy i obejścia wypracowane przy StudentSpot. Ma służyć jako praktyczny wzorzec dla kolejnych aplikacji projektowanych pod AHE Łódź, z zachowaniem spójności wizualnej, dostępności, wersji PL/EN, responsywności oraz gotowości do wdrożenia na Mikrus Frog.

## 1. Najważniejsze założenie

Aplikacja dla AHE powinna wyglądać jak część komunikacji uczelni, ale nie może sugerować, że jest oficjalnym systemem, jeżeli jest projektem studenckim lub prototypem.

Zawsze warto mieć w aplikacji:

- jasny status projektu, np. "Projekt studencki",
- autora i kontekst przedmiotu,
- źródło danych i materiałów graficznych,
- rozdzielenie danych demonstracyjnych od realnych,
- brak sekretów i haseł w repozytorium,
- gotowy plik opisujący oddanie projektu.

## 2. Stack, który sprawdził się na Frog

Najbezpieczniejszy lekki stack:

- Flask,
- Jinja2,
- SQLAlchemy,
- Flask-WTF,
- SQLite lokalnie,
- MySQL / PyMySQL na Frog,
- Gunicorn,
- pytest,
- proste CSS i JS bez ciężkiego frontendu.

Dlaczego:

- Frog ma mało RAM, więc lekki SSR jest rozsądniejszy niż ciężki frontend.
- Jinja2 pozwala szybko utrzymać PL/EN, role i warunki widoczności.
- Flask-WTF daje CSRF i walidację formularzy.
- SQLite wystarcza lokalnie, a `DATABASE_URL` pozwala przejść na MySQL.

Unikać przy małych projektach zaliczeniowych:

- mikroserwisów,
- ciężkiego bundlera,
- rozbudowanego frontendu, jeżeli nie jest konieczny,
- zależności wymagających dużo pamięci,
- trzymania build artefaktów w repo.

## 3. Key visual AHE

Podstawowy kierunek KV został dopasowany do AHE na podstawie publicznego CSS strony uczelni:

```text
view-source:https://www.ahe.lodz.pl//themes/custom/ahe/css/style.css
```

Paleta, która dobrze działa:

```css
--ahe-red: #a91539;
--ahe-navy: #222a56;
--ahe-heading: #343434;
--ahe-text: #515151;
--ahe-muted: #8b8b8b;
--ahe-surface: #f1f1f1;
--ahe-surface-dark: #e2e2e2;
--ahe-border: #bbbbbb;
--ahe-white: #ffffff;
--ahe-black: #000000;
```

Typografia:

```css
--font-ui: "Mundial", Arial, Helvetica, sans-serif;
--font-body: "Neue Haas Grotesk Text Pro", "Helvetica Neue", Arial, sans-serif;
```

Jeżeli fonty uczelni nie są dostępne lokalnie, fallback do Arial / Helvetica jest akceptowalny i stabilny.

## 4. Styl komponentów

Elementy, które najlepiej utrzymały klimat AHE:

- białe tło nagłówka,
- biała, smukła stopka,
- prostokątne panele bez dużych zaokrągleń,
- czerwono-granatowa belka lub cienka linia nad panelem,
- jasnoszare powierzchnie pod treścią,
- granatowe bloki tytułowe dla mocnych nagłówków,
- czerwony jako akcja główna,
- granat jako akcja drugorzędna,
- czarne lub ciemnoszare teksty na jasnym tle.

Warto unikać:

- okrągłych, miękkich kart w stylu SaaS,
- dużych gradientowych plam,
- zbyt wielu cieni,
- dekoracji bez funkcji,
- hero z przypadkową grafiką, jeżeli nie wnosi treści,
- kart w kartach.

Dobry wzorzec sekcji:

```html
<h1 class="page-title">Info</h1>
<section class="panel page-intro">
  ...
</section>
```

Tytuł strony powinien być nad panelem, nie zamknięty w szarym tle. Dzięki temu układ wygląda bliżej komunikacji AHE i jest bardziej elegancki.

## 5. Nagłówek

Najważniejsze wnioski:

- header powinien być biały i smukły,
- logo aplikacji najlepiej jako przycięty prostokąt bez dużych białych marginesów,
- nie dublować obok siebie dużego znaku i osobnego napisu, jeżeli logo zawiera nazwę,
- kliknięcie w logo prowadzi na stronę główną,
- na desktopie elementy powinny trzymać jedną linię,
- na mniejszych ekranach menu może się układać w kilka linii, ale bez nachodzenia.

Praktyczny układ:

```css
.nav {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: clamp(0.45rem, 0.75vw, 0.9rem);
}
```

Problem, który wystąpił:

- link "Media" spadał samotnie do nowej linii.

Obejście:

- zmniejszyć pionowe paddingi headera,
- zastosować `minmax(0, 1fr)` dla środka,
- zmniejszyć logo do kontrolowanego `clamp()`,
- pozwolić menu przejść w układ responsywny dopiero na tablet/mobile,
- testować na szerokim desktopie i typowym laptopie.

## 6. Stopka

Najlepszy wzorzec:

- stopka biała,
- smukła,
- tekst po lewej lub centralnie zależnie od miejsca,
- logotypy po prawej na desktopie,
- logo StudentSpot i AHE dopasowane optycznie wysokością,
- rok pogrubiony.

Tekst:

```text
Projekt studencki: StudentSpot by Paweł Kwaczyński / SKN AIRON / 2026
```

Problem, który wystąpił:

- logotyp AHE był optycznie większy niż StudentSpot.

Obejście:

- nie równać po szerokości, tylko po wysokości znaku,
- przycinać białe marginesy obrazków,
- ustawić `max-height`, a nie stałą szerokość,
- na mobile pozwolić stopce złamać się w dwie linie.

## 7. Logotypy i grafiki

Zasady:

- wszystkie źródła trzymać w `source_info/`,
- wersje używane w aplikacji kopiować do `app/static/media/...`,
- pliki w static nazywać po funkcji, nie po oryginalnym chaotycznym tytule,
- przycinać duże białe marginesy,
- nie mieszać błędnych grafik z właściwymi,
- alt teksty muszą opisywać sens grafiki.

Przykładowe foldery:

```text
app/static/media/brand/
app/static/media/clubs/
app/static/media/news/
app/static/media/people/
app/static/media/rooms/
app/static/media/visuals/
```

Problem, który wystąpił:

- logo z dużym białym marginesem rozwalało wysokość headera i stopki.

Obejście:

- przyciąć margines góra/dół,
- zapisać osobną wersję produkcyjną,
- dopiero ją podpiąć w CSS.

## 8. Strona główna

Najlepszy układ dla projektu AHE:

- mocny nagłówek w granatowych blokach,
- krótki opis pod spodem,
- maksymalnie 2-3 główne akcje,
- grafika powitalna tylko wtedy, gdy nie powoduje pustki i nierówności,
- popup welcome może startować automatycznie na pierwszym wejściu.

Problem, który wystąpił:

- sekcja hero miała za dużo pustego białego miejsca i grafika zasłaniała lub psuła proporcje.

Obejście:

- usunąć prawą grafikę, jeżeli nie jest potrzebna,
- rozciągnąć sekcję tekstową do sensownej szerokości,
- ograniczyć wysokość hero,
- pod sekcją od razu pokazać kolejny kontekst, np. logotypy AHE/Samorządu/UTW albo sale.

## 9. Panele, karty i tagi

Tagi:

- muszą zawijać się elastycznie,
- nie mogą nachodzić na siebie,
- powinny mieć czytelny kontrast,
- przy długich słowach trzeba dopuścić łamanie lub mniejszą szerokość.

Warto stosować:

```css
display: flex;
flex-wrap: wrap;
gap: 0.5rem;
```

Problem:

- tagi typu "psychologia rozwoju" i "pedagogika dziecka" nachodziły na siebie.

Obejście:

- `flex-wrap: wrap`,
- brak stałej wysokości,
- `max-width: 100%`,
- tekst bez ujemnego letter-spacingu,
- test na mobile i tablet.

## 10. Responsywność

Testować minimum:

- telefon: 390 x 844,
- tablet: 1024 x 768,
- desktop: 1440 x 900,
- szeroki desktop: 1920+ lub 2048.

Checklist:

- brak poziomego scrolla,
- header nie nachodzi na treść,
- menu nie ucina ostatnich linków,
- przyciski nie nachodzą na siebie,
- tekst w buttonach mieści się w środku,
- tabele mają overflow lub przechodzą w prostszy układ,
- karty mają sensowną liczbę kolumn,
- popup mieści się w viewport,
- lightbox ma zamykanie i alt.

Przydatne reguły CSS:

```css
body {
  overflow-x: hidden;
}

.container {
  width: min(100% - 2rem, 1180px);
  margin-inline: auto;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: 1rem;
}

img {
  max-width: 100%;
  height: auto;
}
```

Nie skalować fontu przez `vw`. Lepiej:

- `clamp()` dla szerokości elementów,
- stałe rozmiary tekstu przez zmienne,
- `data-font="large"` dla trybu A+.

## 11. Dostępność

Minimalny standard dla kolejnej aplikacji:

- skip link,
- widoczny focus przez `:focus-visible`,
- etykiety formularzy,
- alt teksty obrazów,
- aria-label dla przycisków ikon i lightboxów,
- dialogi z `role="dialog"` i `aria-modal="true"`,
- przyciski mają tekst, nie tylko kolor,
- tryb ciemny,
- wysoki kontrast,
- większa czcionka,
- brak przekazywania informacji kolorem jako jedynym kanałem.

Sprawdzone zmienne:

```css
:root[data-theme="dark"] {
  --bg: #0b1020;
  --surface: #131b2e;
  --surface-strong: #1d2840;
  --text: #f3f7ff;
  --muted: #b6c2d6;
  --border: #34425c;
  --accent: #e33b64;
}

:root[data-contrast="high"] {
  --bg: #ffffff;
  --surface: #ffffff;
  --text: #000000;
  --muted: #111111;
  --border: #000000;
  --accent: #b00020;
  --focus: #0000ff;
}
```

Problem:

- w dark mode część tekstów była bardzo jasna na jasnym panelu albo za słabo kontrastowała.

Obejście:

- każdy panel musi używać zmiennych `--surface`, `--text`, `--muted`, a nie hardcodowanych bieli/szarości,
- tabele muszą mieć osobne style dla dark mode,
- elementy nagłówków w dark mode nie mogą dziedziczyć ciemnego `--ahe-heading`,
- sprawdzić login, demo, info, tabele i formularze w dark mode.

## 12. Dostępność organizacyjna w formularzach

Przy potrzebach dostępnościowych lepiej pisać neutralnie:

- "potrzeby organizacyjne dostępności",
- "tłumacz języka migowego",
- "przewodnik dla osoby niewidomej",
- "bezpłatny transport",
- "sprzęt wspomagający proces dydaktyczny".

Unikać:

- diagnoz,
- szczegółów zdrowotnych,
- pola typu `is_disabled`,
- zbierania danych wrażliwych, jeżeli projekt ich nie potrzebuje.

Dobry tekst pomocniczy:

```text
Podaj wyłącznie potrzeby organizacyjne wydarzenia.
```

## 13. PL/EN

Zasada:

- każdy widoczny tekst przez funkcję tłumaczeń,
- klucze w `app/translations/pl.py` i `app/translations/en.py`,
- brak mieszaniny języków w jednej sekcji,
- wersja EN musi mieć własne assety, jeśli grafika zawiera tekst.

W StudentSpot popup welcome ma osobną wersję PL i EN:

```jinja
{% set popup_asset = 'media/visuals/welcome-popup-en.png' if locale == 'en' else 'media/visuals/welcome-popup.png' %}
```

Checklist PL/EN:

- header,
- footer,
- formularze,
- walidacje,
- popupy,
- alt teksty,
- downloady,
- puste stany,
- opisy techniczne,
- konto użytkownika,
- panel admina.

Problem:

- część komunikatów była poprawiona w PL, ale nie w EN.

Obejście:

- po każdej zmianie tekstu wyszukać klucz w obu plikach tłumaczeń,
- testować `/set-language/en`,
- sprawdzić obrazy z tekstem.

## 14. Popupy i lightbox

Popup welcome:

- może startować automatycznie na stronie głównej,
- powinien mieć przycisk zamknięcia,
- powinien mieć wersję EN, jeśli grafika zawiera tekst,
- nie może zasłaniać permanentnie aplikacji.

Popup rezerwacji:

- dobry do komunikatu "tylko osoba uprawniona może rezerwować salę",
- nie może zastępować kontroli backendowej,
- kontrola uprawnień musi zostać w trasie i usługach.

Lightbox:

- działa dla zdjęć sal, grafik w Info, Media, Aktualnościach i Local Heroes,
- obraz musi mieć `alt`,
- przycisk otwierający powinien być prawdziwym `<button>`.

## 15. Dane demonstracyjne i role

Demo powinno mieć kontrolowane konta i role. Student nie powinien sam wybierać roli przewodniczącego ani administratora.

Przykładowy model:

- `system_admin`,
- `property_admin`,
- `club_guardian`,
- `student`,
- `utw_organizer`.

Role w kole:

- `member`,
- `chair`,
- `vice_chair`,
- `treasurer`,
- `secretary`,
- `guardian`.

Zasady:

- role klubowe potwierdza admin lub opiekun,
- publiczne kontakty opiekunów nie tworzą automatycznie kont,
- rekordy wymagające weryfikacji mogą być w bazie, ale ukryte w katalogu.

## 16. Rezerwacje i sale

Reguły, które działają:

- ograniczyć zakres do konkretnego budynku, jeśli projekt tego wymaga,
- sale sortować alfabetycznie,
- dopasowanie po liczbie osób sortować po najmniejszej sensownej nadwyżce miejsc,
- puste wyniki wyjaśniać, a nie zostawiać pustej strony,
- zdjęcia sal otwierać w lightboxie,
- robocze zdjęcia oznaczać watermarkiem.

Reguła konfliktu czasu:

```text
new_start < existing_end AND new_end > existing_start
```

Uprawnieni do rezerwacji:

- system admin,
- property admin,
- opiekun koła,
- organizator UTW,
- zatwierdzony przewodniczący,
- zatwierdzony zastępca.

## 17. Local Heroes / profile osób

Wzorzec, który wygląda najlepiej:

- duże zdjęcie po lewej,
- po prawej imię i nazwisko,
- pod nim kierunek/specjalność czerwienią AHE,
- niżej bio z dużym interliniowaniem,
- brak ramek w ramkach,
- cały blok szeroki i spokojny.

Problem:

- układ kartowy wyglądał zbyt mało "AHE" i miał za dużo powtarzalnych ramek.

Obejście:

- użyć pełnych bloków biograficznych,
- zachować dużo oddechu,
- ustawić zdjęcia w jednej proporcji,
- na mobile układać zdjęcie nad tekstem.

## 18. Media i materiały do pobrania

Zakładka Media powinna zawierać:

- krótką notatkę prasową,
- logo aplikacji,
- grafiki welcome/popup,
- logotypy AHE, Samorządu, UTW, jeśli są potrzebne,
- przyciski pobierania,
- lightbox po kliknięciu grafiki.

Nie mieszać w Media:

- danych autora, jeżeli są już w Info,
- key visual, jeżeli jest już w Info,
- grafik osób, jeżeli mają własną zakładkę Local Heroes.

## 19. Strona Info dla projektu zaliczeniowego

Dobrze działa mapa wymagań projektowych:

1. miejsce użytkowania i organizacja,
2. problem i kontekst systemu,
3. użytkownicy, role i uprawnienia,
4. założenia i zależności,
5. wymagania funkcjonalne,
6. wymagania niefunkcjonalne,
7. projekt koncepcyjny i przepływy informacyjne.

Warto jawnie opisać:

- autora,
- ID studenta,
- afiliację,
- opiekuna przedmiotu,
- źródło KV,
- status prototypu,
- ograniczenia demo.

Dokumenty wynikowe mogą być rekordami systemowymi:

- wniosek członkowski,
- wniosek rezerwacyjny,
- decyzja statusowa,
- powiadomienie,
- wpis audytu,
- plik `.ics`.

## 20. Frog / Mikrus

Najważniejsze parametry:

- system: Alpine Linux,
- RAM: 256 MB,
- dysk: 3 GB,
- baza: współdzielony MySQL,
- publiczny HTTPS przez `wykr.es`,
- aplikacja nasłuchuje HTTP na przydzielonym porcie,
- nie używać domyślnego portu 80,
- nie skanować portów.

Adres publiczny:

```text
https://frog01-APP_PORT.wykr.es
```

Minimalny start:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo
gunicorn --workers 1 --threads 2 --timeout 60 --bind 0.0.0.0:${APP_PORT} wsgi:app
```

Zmienne środowiskowe:

```env
SECRET_KEY=wstaw-dlugi-losowy-sekret
DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE?charset=utf8mb4
APP_PORT=12345
SHOW_DEV_ACTIVATION_CODE=0
```

Zasady:

- `.env` tylko na serwerze,
- haseł nie wpisywać do repo,
- lokalne notatki z dostępami kończyć jako `*.local.md`,
- `docs/*.local.md` dodać do `.gitignore`,
- ZIP też musi wykluczać lokalne notatki i `.env`.

## 21. Pakowanie projektu

Dobre wykluczenia ZIP:

```text
.git/
.venv/
__pycache__/
.pytest_cache/
instance/
docs/*.local.md
.env
.env.local
.env.production
student_spot*.zip
```

Dla paczki profesorskiej dodatkowo można wykluczyć:

```text
PROGRESS.md
IMPLEMENTATION_PLAN.md
```

Warto mieć dwa skrypty:

- pełna paczka robocza,
- paczka do oddania.

## 22. Testy i QA

Minimum przed oddaniem:

```bash
python -m compileall app tests
python -m pytest
flask --app wsgi:app routes
```

Smoke test przeglądarkowy:

- strona główna,
- login,
- rejestracja,
- konto użytkownika,
- katalog,
- formularz,
- panel admina,
- Info,
- Media,
- PL/EN,
- dark mode,
- kontrast,
- A+,
- mobile i tablet.

Szukaj:

- poziomego scrolla,
- nachodzących tagów,
- spadającego menu,
- za dużych białych przestrzeni,
- jasnego tekstu w dark mode,
- brakujących altów,
- niedziałającego lightboxa,
- pustych wyników bez komunikatu.

## 23. Bezpieczeństwo i prywatność

Zasady bazowe:

- hasła tylko jako hash,
- CSRF w formularzach,
- tokeny aktywacyjne hashowane lub krótkotrwałe,
- brak sekretów w repo,
- brak prywatnych danych w logach,
- brak danych medycznych, jeżeli aplikacja ich nie potrzebuje,
- role sprawdzane po stronie backendu,
- demo konta jasno oznaczone jako demonstracyjne.

W opisach dostępności nie zbierać diagnoz ani statusu osoby. Zapisywać wyłącznie potrzeby organizacyjne wydarzenia.

## 24. Problemy, które warto pamiętać

1. Header z dużym logo szybko robi się zbyt wysoki.
   Rozwiązanie: przycięte logo, biały slim header, kontrolowany `max-height`.

2. Linki menu mogą spadać w dziwne miejsca.
   Rozwiązanie: grid headera, `minmax(0, 1fr)`, krótsze odstępy, osobne reguły mobile.

3. Dark mode łatwo psuje tabele i formularze.
   Rozwiązanie: używać zmiennych kolorów, nie hardcodować białych paneli.

4. Grafiki z tekstem muszą mieć wersję EN.
   Rozwiązanie: wybór assetu po `locale`.

5. Tagi w kartach nachodzą na siebie.
   Rozwiązanie: `flex-wrap`, brak stałych wysokości, test mobile.

6. Paczka ZIP może złapać prywatne notatki.
   Rozwiązanie: `.gitignore` i wykluczenia w skryptach pakujących.

7. Równoległe pakowanie ZIP potrafi złapać tymczasowy plik drugiej paczki.
   Rozwiązanie: pakować sekwencyjnie, nie równolegle.

8. Publiczne źródła AHE mogą mieć stare dane.
   Rozwiązanie: pokazywać publicznie tylko potwierdzone rekordy, a pozostałe trzymać w panelu administratora do ręcznej weryfikacji.

9. Tekst "apel" lub podobne określenia mogą brzmieć niejasno.
   Rozwiązanie: neutralne "komunikat do UTW" albo "powiadomienie".

10. Duże grafiki mogą tworzyć pustą stronę.
    Rozwiązanie: grafika tylko, gdy wspiera treść; inaczej mocny tekst i szybkie przejście do kolejnej sekcji.

## 25. Checklist dla kolejnej aplikacji AHE

Przed developmentem:

- określić, czy projekt jest oficjalny czy studencki,
- zebrać logotypy i KV,
- ustalić źródła danych,
- ustalić role użytkowników,
- zaprojektować PL/EN od początku,
- wybrać lekki stack pod Frog.

Podczas developmentu:

- trzymać style w zmiennych CSS,
- robić komponenty prostokątne i czytelne,
- testować mobile/tablet/desktop co kilka większych zmian,
- aktualizować oba języki jednocześnie,
- dodawać alt i aria przy grafikach/dialogach,
- nie hardcodować sekretów,
- pisać testy dla głównych procesów.

Przed oddaniem:

- uruchomić testy,
- zrobić smoke test przeglądarkowy,
- sprawdzić ZIP,
- sprawdzić brak `.env` i lokalnych dostępów,
- sprawdzić brak roboczych plików procesu,
- przygotować dokument oddania,
- przygotować instrukcję Frog,
- zapisać commit i wypchnąć repo.

## 26. Minimalny szablon nowych projektów

Struktura:

```text
app/
  static/
    css/
    js/
    media/
  templates/
  translations/
docs/
source_info/
tests/
migrations/
scripts/
README.md
.env.example
.gitignore
wsgi.py
```

Pliki obowiązkowe:

- `README.md`,
- `docs/FROG_DEPLOYMENT.md`,
- `docs/ODDANIE_PROJEKTU.md`,
- `scripts/package_release.sh`,
- `scripts/package_professor_release.sh`,
- `.env.example`,
- testy głównych procesów.

## 27. Krótka reguła końcowa

Jeżeli kolejna aplikacja ma wyglądać spójnie z AHE, trzymaj się prostych prostokątów, białego nagłówka, czerwieni `#A91539`, granatu `#222A56`, jasnych powierzchni, mocnych nagłówków, dobrej responsywności i pełnej dostępności. Najpierw ma działać proces, dopiero potem dekoracja.
