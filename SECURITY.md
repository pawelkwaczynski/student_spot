# Security Policy

## Reporting a vulnerability

Please do not disclose security issues publicly if they include exploit details, credentials, private data, server configuration or personal information.

Send a private report to:

```text
kwaczynski.pawel@gmail.com
```

Include:

- affected route, role or workflow,
- steps to reproduce,
- expected and actual behavior,
- potential impact,
- suggested fix, if known.

## Scope

StudentSpot is a student project and open-source prototype. The public demo uses fictional demo data. Reports about authentication, authorization, CSRF, stored data exposure, unsafe file handling, dependency risks and deployment configuration are welcome.

## Out of scope

- Social engineering.
- Denial-of-service testing.
- Port scanning or infrastructure scanning.
- Testing with real student, medical or sensitive personal data.

## Security principles

- Secrets must stay in environment variables or private deployment notes.
- Passwords and activation tokens must never be stored as plain text.
- Role checks must be enforced on the server side.
- Demo data must stay fictional.
- Accessibility support fields should describe organization needs only, not diagnoses.
