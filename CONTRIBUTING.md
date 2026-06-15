# Contributing

Thanks for your interest in StudentSpot.

## How to contribute

1. Fork the repository.
2. Create a small, focused branch.
3. Install dependencies and run the tests.
4. Keep demo data fictional.
5. Open a pull request with a short description of the change and its user-facing impact.

## Local setup

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo
flask --app wsgi:app run --port 8000
```

## Quality checks

```bash
python -m compileall app tests
python -m pytest
python -m pip check
```

## Data rules

- Do not commit secrets, passwords, access notes or `.env` files.
- Do not add real student, health or disability diagnosis data.
- Keep accessibility fields focused on event organization needs.
- Keep PL and EN text consistent when changing user-facing copy.
