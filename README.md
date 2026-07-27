# StudentSpot

StudentSpot is an open-source platform for student organizations, campus accessibility and room management. It helps student clubs publish their profile, manage membership requests, send messages, find accessible rooms, submit room reservations and export approved meetings to a calendar file.

StudentSpot is not an official AHE system. It shows how a lightweight management information system can support campus coordination with accessibility, bilingual UI and clear role-based workflows.

Live instance:

```text
https://frog01-20412.wykr.es
```

## Why it matters

Student organizations often coordinate events across scattered emails, chat threads, spreadsheets and informal room requests. That creates friction for club leaders, guardians, property administrators and students who need accessible participation options.

StudentSpot turns that process into one coherent flow:

- discover student organizations and recommended clubs,
- submit or review membership requests,
- manage club roles and communication,
- search rooms by capacity, equipment and accessibility needs,
- request a room and detect schedule conflicts,
- approve or reject reservations with an auditable status history,
- export approved meetings to `.ics`,
- keep the interface usable in PL/EN, dark mode, high contrast and larger text modes.

## Features (current scope)

- Rooms limited to the Sterlinga 26 building.
- PL/EN interface, dark mode, high contrast, larger font.
- Two-step registration with e-mail activation, consents and club selection.
- Membership requests and admin/guardian decisions.
- Room catalog with photos, filters, building map and best-capacity matching.
- Catalog of 7 public AHE clubs plus hidden records awaiting admin confirmation.
- Reservations with conflict detection, admin decisions and status history.
- `.ics` export of approved meetings.
- `/news`, `/calendar`, `/local-heroes`, `/info` and `/media` pages.
- In-app messaging: guardians message approved club members.
- UTW organizer accounts and admin announcements.
- In-app notifications and a basic audit log.

## Roadmap

- Alembic migrations for long-term schema evolution.
- E-mail delivery for activation links and notifications.
- Recurring reservations and calendar subscription feeds.
- Richer organization pages for public university communities.
- WCAG audit notes and automated accessibility checks.
- API endpoints for room availability and club data.
- Deployment recipes for low-resource VPS, Docker and managed platforms.

## Local development

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
flask --app wsgi:app init-db --reset
flask --app wsgi:app seed-demo   # development/test data only
flask --app wsgi:app run --port 8000
```

Open `http://127.0.0.1:8000`.

## Production setup

Production uses a single canonical database: MySQL configured via `DATABASE_URL` in `.env` (see `.env.example`). SQLite is a local development fallback only.

```bash
flask --app wsgi:app init-db
flask --app wsgi:app seed-catalog                      # majors, clubs, rooms — no user accounts
flask --app wsgi:app create-admin --email admin@example.com   # prompts for a password
gunicorn --workers 1 --threads 2 --timeout 60 --bind 0.0.0.0:${APP_PORT} wsgi:app
```

Deployment details: `docs/FROG_DEPLOYMENT.md`.

## Tests

```bash
. .venv/bin/activate
python -m pytest
```

## Contributing

Contributions are welcome. Good first areas are documentation, tests, accessibility improvements, translations, UI polish and small Flask/Jinja2 features. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

Please do not report security issues in public issues if they include exploit details, private data, credentials or server-specific information. Send a private report to the maintainer instead. See [SECURITY.md](SECURITY.md).

Security principles:

- passwords and activation tokens are hashed,
- forms use CSRF protection,
- seeded data must stay fictional,
- real medical or disability diagnoses must not be collected,
- access control must be enforced server-side,
- `.env`, local access notes and credentials must stay out of Git.

## License

StudentSpot is released under the [MIT License](LICENSE).
