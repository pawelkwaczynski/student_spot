# StudentSpot - opis do oddania projektu

## Dane projektu

- Nazwa: StudentSpot
- Autor: Paweł Kwaczyński
- ID studenta: 165318
- E-mail: kwaczynski.pawel@gmail.com
- Afiliacja: członek Studenckiego Koła Naukowego AIRON
- Przedmiot: Podstawy systemów informatycznych zarządzania / Metodyka zarządzania informacją
- Opieka merytoryczna: prof. dr hab. Marian Niedźwiedziński

## Repozytorium

```text
https://github.com/pawelkwaczynski/student_spot
```

## Zakres aplikacji

StudentSpot jest nieoficjalnym prototypem studenckim dla środowiska AHE w Łodzi. Aplikacja wspiera katalog kół naukowych, wybór koła, listę członków u opiekuna, zatwierdzanie statusów i ról, wiadomości do członków koła, rezerwacje sal w budynku Sterlinga 26, decyzje administracyjne, powiadomienia, eksport spotkania do kalendarza oraz ustawienia dostępności.

Projekt zawiera dwie wersje językowe PL/EN, tryb ciemny, wysoki kontrast, większą czcionkę, responsywny układ desktop/tablet/mobile oraz dane demonstracyjne.

## Uruchomienie lokalne

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo
flask --app wsgi:app run --port 8000
```

Adres lokalny:

```text
http://127.0.0.1:8000
```

## Konta demo

Hasło dla wszystkich kont:

```text
StudentSpot123!
```

| Konto | Rola |
|---|---|
| admin@studentspot.example.com | system admin |
| property@studentspot.example.com | property admin |
| guardian@studentspot.example.com | opiekun koła |
| boss@studentspot.example.com | przewodniczący / chair |
| vice@studentspot.example.com | vice chair |
| member@studentspot.example.com | zwykły członek |
| pending@studentspot.example.com | oczekujący student |
| utw@studentspot.example.com | UTW organizer |

## Frog / Mikrus

Planowane środowisko wdrożeniowe:

- VPS: Mikrus Frog
- serwer: frog01.mikr.us
- port SSH: 10412
- publiczny adres po uruchomieniu aplikacji: `https://frog01-APP_PORT.wykr.es`
- baza docelowa: współdzielony MySQL Froga, dane dostępowe z `/root/mysql.txt`
- proces aplikacji: Gunicorn na przydzielonym porcie `APP_PORT`

Hasła, plik `.env` i dane dostępowe do bazy nie są umieszczane w repozytorium ani w paczce ZIP.

Szczegóły wdrożenia są w pliku:

```text
docs/FROG_DEPLOYMENT.md
```

## Dokumenty wynikowe w prototypie

W projekcie dokumenty wynikowe mają formę rekordów systemowych i widoków aplikacji:

- wniosek członkowski: rekord `ClubMembership`,
- wniosek rezerwacyjny: rekord `Reservation`,
- decyzja statusowa: historia statusu i decyzja admina,
- wiadomość opiekuna do członków koła: rekord `ClubMessage` i rekordy odbiorców `ClubMessageRecipient`,
- powiadomienie: rekord `Notification`,
- wpis audytu: rekord `AuditLog`,
- plik kalendarza: eksport `.ics` dla zatwierdzonego spotkania.

## Testy

```bash
. .venv/bin/activate
python -m compileall app tests
python -m pytest
```

## Paczka do oddania

Paczka profesorska jest tworzona komendą:

```bash
bash scripts/package_professor_release.sh
```

Wynik:

```text
student_spot_profesor.zip
```

Paczka nie zawiera lokalnej bazy, środowiska `.venv`, cache, prywatnych notatek dostępowych, pliku `.env` ani roboczych checkpointów.

## Dodatkowe pliki pomocnicze

- `prezentacja_ustna_10_min.md` - scenariusz prezentacji na zajęcia.
- `plan_pokazowy_student_spot.md` - praktyczna kolejność demo funkcji aplikacji.
- `student_spot_dev_handoff.zip` - neutralna paczka techniczno-wizualna do utrzymania spójności kolejnych projektów AHE.
