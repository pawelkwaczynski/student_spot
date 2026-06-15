# Plan pokazowy StudentSpot

## Cel demo

Pokazać StudentSpot jako działający system informatyczny wspierający zarządzanie kołami naukowymi AHE: członkostwo, role, rezerwacje sal, decyzje administracyjne, wiadomości, kalendarz, aktualności i dostępność.

## Start techniczny

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo
flask --app wsgi:app run --port 8000
```

Adres:

```text
http://127.0.0.1:8000
```

Hasło do kont demo:

```text
StudentSpot123!
```

## Kolejność pokazu

1. **Start**
   - pokaż logo StudentSpot i logotypy AHE/Samorząd/UTW,
   - pokaż popup welcome,
   - pokaż sale, 7 publicznych kół i feed aktualności pod kołami,
   - powiedz: system porządkuje proces od odkrycia koła do rezerwacji i decyzji administracyjnej.

2. **Info**
   - pokaż mapę wymagań projektowych,
   - pokaż opis organizacji, problem, role, założenia, wymagania funkcjonalne i niefunkcjonalne,
   - pokaż opis KV AHE i źródło dopasowania wizualnego.

3. **Demo**
   - pokaż 8 kont demo,
   - pokaż tabelę: kto co może zrobić,
   - przejdź według tutoriala na stronie.

4. **Opiekun koła**
   - zaloguj: `guardian@studentspot.example.com`,
   - wejdź w `/admin/`,
   - pokaż oczekujące wnioski członkowskie,
   - pokaż pełną listę członków koła,
   - pokaż zmianę roli i statusu,
   - pokaż przycisk wiadomości.

5. **Wiadomości**
   - jako opiekun wejdź w `/messages/compose`,
   - wybierz AIrON,
   - wyślij krótką wiadomość do członków,
   - wyloguj się i zaloguj jako `boss@studentspot.example.com`,
   - wejdź w `/messages/` i pokaż odebraną wiadomość.

6. **Rezerwacja sali**
   - jako przedstawiciel koła wejdź w `/reservations/new`,
   - pokaż modal informujący o uprawnieniach,
   - pokaż pola: koło, sala, data, godziny, uczestnicy,
   - pokaż wymagania dostępnościowe: tłumacz języka migowego, przewodnik, transport z terenu Łodzi, sprzęt wspomagający,
   - wyślij rezerwację do kolejki administracyjnej.

7. **Property admin**
   - zaloguj: `property@studentspot.example.com`,
   - wejdź w `/admin/`,
   - pokaż oczekujące rezerwacje,
   - pokaż zatwierdzanie/odrzucanie rezerwacji,
   - pokaż ukryte koła do potwierdzenia,
   - pokaż komunikat do UTW.

8. **Student bez uprawnień**
   - zaloguj: `member@studentspot.example.com`,
   - spróbuj wejść w `/reservations/new`,
   - pokaż, że zwykły członek nie rezerwuje sal bez roli przedstawiciela.

9. **Kalendarz i ICS**
   - pokaż `/calendar`,
   - pokaż przykładowe sloty czerwiec/lipiec 2026,
   - pokaż zatwierdzoną rezerwację i link `Dodaj do kalendarza`.

10. **Aktualności, Local Heroes, Media**
    - pokaż `/news`,
    - pokaż `/local-heroes`,
    - pokaż `/media` i pliki do pobrania,
    - pokaż lightbox grafik.

11. **Dostępność i responsywność**
    - przełącz PL/EN,
    - włącz tryb ciemny,
    - włącz kontrast,
    - włącz A+,
    - zwęż okno do telefonu i pokaż brak poziomego przewijania.

## Logika ról

| Konto | Rola | Najważniejsze uprawnienia |
|---|---|---|
| admin@studentspot.example.com | system admin | pełna administracja, członkostwa, rezerwacje, koła, audyt |
| property@studentspot.example.com | property admin | rezerwacje sal, ukryte koła do potwierdzenia, komunikat UTW |
| guardian@studentspot.example.com | opiekun koła | członkowie koła, statusy, role, wiadomości do członków |
| boss@studentspot.example.com | przedstawiciel koła | rezerwacje w imieniu koła, moje konto, skrzynka |
| vice@studentspot.example.com | przedstawiciel koła | rezerwacje w imieniu koła, eksport ICS |
| member@studentspot.example.com | zwykły członek | przeglądanie, moje konto, brak rezerwacji |
| pending@studentspot.example.com | oczekujący student | oczekuje na decyzję opiekuna/admina |
| utw@studentspot.example.com | UTW organizer | rezerwacje i odbiór komunikatów UTW |

## Stack technologiczny

- Python
- Flask
- Jinja2
- SQLAlchemy
- SQLite lokalnie
- PyMySQL na Frog
- Flask-WTF i CSRF
- HTML/CSS/JavaScript bez ciężkiego frontendu
- pytest
- Gunicorn na serwerze

## Najważniejsze zdanie końcowe

StudentSpot pokazuje kompletny przepływ informacji w organizacji edukacyjnej: od użytkownika i roli, przez wniosek i decyzję, po powiadomienie, audyt i dokument wynikowy.
