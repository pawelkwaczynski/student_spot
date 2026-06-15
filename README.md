# StudentSpot

StudentSpot to lekka aplikacja Flask/Jinja2 do demonstracyjnego zarzadzania kolami naukowymi, czlonkostwami, salami i rezerwacjami. Projekt jest przygotowany jako nieoficjalny prototyp studencki.

## Zakres demo

- Tylko sale i budynek przy ul. Sterlinga 26.
- Interfejs PL/EN.
- Dark mode, wysoki kontrast i wieksza czcionka.
- Rejestracja, aktywacja konta, logowanie.
- Rejestracja 2-krokowa: dane studenckie, bezpieczenstwo, zgody, status `pending_verification`, potwierdzenie e-maila i ekran wyboru kola.
- Wnioski czlonkowskie i decyzje administratora/opiekuna.
- Katalog sal ze zdjeciami, filtrowaniem i mapa budynku.
- Dopasowanie sal po liczbie osob: najpierw sale z najmniejsza sensowna nadwyzka miejsc.
- Katalog 7 publicznie pokazanych kol AHE oraz 6 ukrytych rekordow do potwierdzenia przez admina.
- Rezerwacje sal, konflikt terminow, decyzje admina i historia statusow.
- Eksport zatwierdzonego spotkania kola do pliku `.ics`.
- Strona `/news` z templatkami aktualnosci kol naukowych na podstawie paczki blogowej.
- Strona `/calendar` z demonstracyjnymi rezerwacjami sal na czerwiec/lipiec 2026.
- Strona `/info` z kontekstem projektu, danymi autora, zrodlem KV AHE z `view-source`, modelem UTW oraz jawna mapa wymagan projektowych: organizacja, problem, role, zalozenia, wymagania funkcjonalne, niefunkcjonalne i przeplywy informacyjne.
- Strona `/demo` z kontami demo, opisem projektu i tech stackiem.
- Strona `/media` z notatka prasowa oraz downloadami logo, grafiki welcome i logotypow AHE/Samorzadu/UTW.
- Strona `/local-heroes` z demonstracyjnymi profilami lokalnych liderow, ambasadorow i ekspertow AHE.
- Lightbox zdjec sal oraz znak wodny `TEMPLATRE` dla roboczych sal komputerowych K200A/K320.
- Lightbox grafik na stronach Info, Media, Aktualnosci i Local Heroes.
- Panel admina/opiekuna do potwierdzania danych kol, obslugi wnioskow czlonkowskich, listy czlonkow kola, zmiany statusu/roli oraz wysylania wiadomosci do czlonkow.
- Skrzynka wiadomosci w aplikacji: opiekun kola wysyla komunikat do zatwierdzonych czlonkow, a czlonek odbiera go w `/messages`.
- Panel admina do wysylania komunikatow do kont UTW.
- Powiadomienia w aplikacji i podstawowy audyt.
- Plik `prezentacja_ustna_10_min.md` z gotowym scenariuszem prezentacji przed profesorem.

## Szybki start lokalny

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo
flask --app wsgi:app run --port 8000
```

Otworz:

```text
http://127.0.0.1:8000
```

Publiczne demo na Mikrus Frog:

```text
https://frog01-20412.wykr.es
```

## Konta demo

Wszystkie konta maja haslo:

```text
StudentSpot123!
```

| Konto | Rola |
|---|---|
| admin@studentspot.example.com | administrator systemu |
| property@studentspot.example.com | administrator nieruchomosci |
| guardian@studentspot.example.com | opiekun kola |
| boss@studentspot.example.com | przewodniczacy AIrON |
| vice@studentspot.example.com | wiceprzewodniczacy AIrON |
| member@studentspot.example.com | zwykly czlonek kola |
| pending@studentspot.example.com | student z oczekujacym wnioskiem |
| utw@studentspot.example.com | organizator UTW |

## Testy

```bash
. .venv/bin/activate
python -m pytest
```

Aktualnie testy sprawdzaja m.in. seed 8 kont, 13 kol AHE, ukrywanie kol wymagajacych weryfikacji, ograniczenie sal do Sterlinga, rejestracje, aktywacje, duplikaty, uprawnienia, filtrowanie sal i kol, najlepsze dopasowanie pojemnosci, konflikt rezerwacji, potrzeby dostepnosciowe, eksport `.ics`, komunikat UTW, decyzje admina, pelna liste czlonkow u opiekuna, wiadomosci do czlonkow, audyt, strony `/news`, `/calendar`, `/local-heroes` oraz polska i angielska wersje mapy wymagan projektowych w `/info`.

## Materialy zrodlowe

Folder `source_info/` przechowuje materialy dostarczone do projektu, w tym wytyczne KV AHE, dane kol naukowych, paczke `studentspot_people_package.zip`, paczke `blog_package.zip` oraz dokument `Prezentacja i projekt ZDW_latest.docx`. Interfejs KV zostal dopasowany do AHE na podstawie CSS strony AHE wskazanego w `/info`.

## Pakowanie ZIP

Paczka dla profesora:

```bash
bash scripts/package_professor_release.sh
```

Wynik:

```text
student_spot_profesor.zip
```

Pełna paczka robocza:

```bash
bash scripts/package_release.sh
```

Skrypt tworzy:

```text
student_spot.zip
```

Paczka dev handoff do przenoszenia stylu AHE/KV i dobrych praktyk do kolejnych projektow:

```bash
bash scripts/package_dev_handoff.sh
```

Wynik:

```text
student_spot_dev_handoff.zip
```

Do ZIP nie trafia `.venv`, cache Pythona, lokalna baza SQLite, lokalne notatki z dostępami, plik `.env` ani pliki systemowe `.DS_Store`.

## Wdrozenie Frog

Szczegolowa instrukcja jest w:

```text
docs/FROG_DEPLOYMENT.md
```

Minimalny start Gunicorn na Frog:

```bash
gunicorn --workers 1 --threads 2 --timeout 60 --bind 0.0.0.0:${APP_PORT} wsgi:app
```

Aktualne demo dziala na porcie `20412` i korzysta z SQLite w katalogu aplikacji. Konfiguracja MySQL przez `DATABASE_URL` zostaje opisana jako wariant docelowy w dokumentacji.

## Wazne zasady

- To nie jest oficjalny system AHE.
- Nie zbieramy danych medycznych; wymagania dostepnosciowe opisuja organizacje wydarzenia.
- Sekrety sa tylko w zmiennych srodowiskowych.
- Produkcyjny SMTP i MySQL wymagaja konfiguracji w `.env`.
