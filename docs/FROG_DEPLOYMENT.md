# StudentSpot - wdrozenie na Mikrus Frog

Instrukcja zaklada Alpine Linux, przydzielony port aplikacji w `APP_PORT` oraz wspoldzielony MySQL Froga.

## 1. Wgranie plikow

Wgraj `student_spot.zip` na konto Frog i rozpakuj:

```bash
unzip student_spot.zip -d student_spot
cd student_spot
```

## 2. Pakiety systemowe

```bash
apk add --no-cache python3 py3-pip python3-dev build-base mariadb-client
```

## 3. Virtualenv

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Konfiguracja `.env`

Skopiuj przyklad:

```bash
cp .env.example .env
```

Dane MySQL na Frogu zwykle sa w:

```bash
cat /root/mysql.txt
```

Ustaw `DATABASE_URL` w formacie:

```text
mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE?charset=utf8mb4
```

Przyklad:

```env
SECRET_KEY=wstaw-dlugi-losowy-sekret
DATABASE_URL=mysql+pymysql://frog_user:password@mysql:3306/frog_db?charset=utf8mb4
APP_PORT=12345
SHOW_DEV_ACTIVATION_CODE=0
```

SMTP ustaw tylko jezeli jest dostepny. Nie wpisuj hasel do repozytorium.

## 5. Inicjalizacja bazy

```bash
. .venv/bin/activate
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo
```

Na produkcji nie wykonuj `--reset`, jezeli baza zawiera realne dane.

## 6. Start aplikacji

```bash
export APP_PORT=12345
gunicorn --workers 1 --threads 2 --timeout 60 --bind 0.0.0.0:${APP_PORT} wsgi:app
```

Publiczny adres ma postac:

```text
https://frogXX-PORT.wykr.es
```

Aplikacja sama slucha HTTP. HTTPS zapewnia infrastruktura `wykr.es`.

## 7. Health check

```bash
curl http://127.0.0.1:${APP_PORT}/health
```

Oczekiwany wynik:

```json
{"service":"studentspot","status":"ok"}
```

## 8. Logi i restart

Tryb prosty:

```bash
pkill -f 'gunicorn.*wsgi:app'
gunicorn --workers 1 --threads 2 --timeout 60 --bind 0.0.0.0:${APP_PORT} wsgi:app
```

W praktycznym wdrozeniu warto uruchomic proces w `tmux`, `screen` albo pod prostym nadzorem dostepnym na koncie.

## 9. Backup bazy

```bash
mysqldump -h HOST -u USER -p DATABASE > backup_studentspot.sql
```

## 10. Checklist przed oddaniem

- `.env` istnieje na serwerze i nie jest w ZIP jako sekret.
- `SECRET_KEY` jest zmieniony.
- `SHOW_DEV_ACTIVATION_CODE=0` dla publicznego wdrozenia.
- `/health` odpowiada.
- Logowanie dziala dla kont demo.
- Katalog sal pokazuje tylko Sterlinga 26.
- Panel admina pozwala zatwierdzic/odrzucic rezerwacje.
