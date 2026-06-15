from __future__ import annotations

from app.models import Club


CLUB_LOGOS: dict[str, str] = {
    "airon": "media/clubs/airon-logo.png",
    "kognitywistyczno-eksperymentalne": "media/clubs/kognitywistyka-logo.png",
    "grafika": "media/clubs/grafika-logo.webp",
    "warsztaty-emocji": "media/clubs/arteterapia-logo.webp",
    "progressus": "media/clubs/progressus-logo.webp",
    "wkreceni": "media/clubs/wkreceni-logo.webp",
    "pedagogika-dziecka": "media/clubs/pedagogika-dziecka-logo.png",
}

SQUARE_LOGO_SLUGS = {"warsztaty-emocji", "pedagogika-dziecka"}


def club_logo_url(club: Club | None) -> str | None:
    if not club or not club.slug:
        return None
    return CLUB_LOGOS.get(club.slug)


def club_logo_is_square(club: Club | None) -> bool:
    return bool(club and club.slug in SQUARE_LOGO_SLUGS)
